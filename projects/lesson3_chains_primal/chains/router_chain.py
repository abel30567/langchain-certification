"""
Router Chain - Routes questions to specialized Primal TCG expert chains
Demonstrates MultiPromptChain and LLMRouterChain
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
import os
from dotenv import load_dotenv

load_dotenv()


class PrimalTCGRouterChain:
    def __init__(self, temperature: float = 0.7):
        self.llm = ChatOpenAI(temperature=temperature, model="gpt-3.5-turbo")
        self.router_llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")  # Zero temp for routing
        self.verbose = True
        
        # Create the router chain
        self.router_chain = self._create_router_chain()
    
    def _create_expert_templates(self):
        """Create templates for different expert systems"""
        
        rules_template = """You are a Primal TCG rules expert with deep knowledge of the comprehensive rulebook.
You excel at answering questions about game mechanics, timing, triggers, and interactions.
You always cite specific rules when applicable and explain complex interactions clearly.

Key areas of expertise:
- Turn structure and phases
- TRIGGER ability timing and stacking
- Combat mechanics (Leader/Support values)
- Resource management (cards under/attached)
- Skill and element interactions

Question: {input}

Provide a detailed rules-based answer:"""

        deckbuilding_template = """You are a master Primal TCG deck builder with extensive experience in competitive play.
You specialize in optimizing deck compositions, mana curves, and card synergies.
You understand the meta-game and can recommend cards for any strategy.

Key areas of expertise:
- Deck composition and ratios
- Mana curve optimization
- Synergy identification
- Sideboard construction
- Meta-game positioning
- Card evaluation and substitutions

Question: {input}

Provide deck building advice:"""

        strategy_template = """You are a professional Primal TCG player and strategy coach.
You excel at game planning, combo execution, and matchup analysis.
You can break down complex plays and explain optimal lines of play.

Key areas of expertise:
- Turn-by-turn game plans
- Combo identification and execution
- Matchup analysis (aggro/control/combo/midrange)
- Mulligan decisions
- Resource management
- Bluff and mind games
- Tournament preparation

Question: {input}

Provide strategic analysis:"""

        meta_template = """You are a Primal TCG meta-game analyst and data expert.
You track tournament results, analyze deck performance, and predict meta shifts.
You understand deck popularity, win rates, and how to counter popular strategies.

Key areas of expertise:
- Current meta-game trends
- Deck tier rankings
- Tournament results analysis
- Counter-meta deck building
- Format health assessment
- Ban/restriction impact analysis

Question: {input}

Provide meta-game analysis:"""

        trading_template = """You are a Primal TCG card trader and market analyst.
You understand card values, market trends, and investment opportunities.
You can evaluate trades, predict price movements, and identify undervalued cards.

Key areas of expertise:
- Card pricing and valuation
- Market trend analysis
- Trade evaluation
- Investment recommendations
- Rarity and print run impacts
- Tournament impact on prices

Question: {input}

Provide trading/market advice:"""

        beginner_template = """You are a friendly Primal TCG teacher specializing in helping new players.
You explain concepts simply, avoid jargon, and build understanding step-by-step.
You're patient and encouraging, making the game accessible to everyone.

Key areas of expertise:
- Basic game rules and flow
- Starter deck recommendations
- Simple strategies
- Common mistakes to avoid
- Learning progression path
- Budget-friendly options

Question: {input}

Provide beginner-friendly guidance:"""

        lore_template = """You are a Primal TCG lore master and story expert.
You know the background of every character, the history of each faction, and the narrative behind card abilities.
You can explain how card mechanics relate to their lore and the overall story.

Key areas of expertise:
- Character backgrounds and relationships
- Faction histories (PIRATE, SIN, MICROMON, etc.)
- Story progression through sets
- Flavor text interpretation
- Mechanical-lore connections
- World-building elements

Question: {input}

Provide lore and story information:"""

        return [
            {
                "name": "rules_expert",
                "description": "Expert on game rules, mechanics, timing, and technical interactions",
                "prompt_template": rules_template
            },
            {
                "name": "deckbuilding_expert",
                "description": "Expert on deck construction, optimization, and card synergies",
                "prompt_template": deckbuilding_template
            },
            {
                "name": "strategy_expert",
                "description": "Expert on gameplay strategy, combos, and matchup analysis",
                "prompt_template": strategy_template
            },
            {
                "name": "meta_expert",
                "description": "Expert on meta-game trends, tournament results, and format analysis",
                "prompt_template": meta_template
            },
            {
                "name": "trading_expert",
                "description": "Expert on card values, market trends, and trading advice",
                "prompt_template": trading_template
            },
            {
                "name": "beginner_expert",
                "description": "Expert on teaching new players and explaining basics simply",
                "prompt_template": beginner_template
            },
            {
                "name": "lore_expert",
                "description": "Expert on card lore, story, and world-building",
                "prompt_template": lore_template
            }
        ]
    
    def _create_router_chain(self) -> MultiPromptChain:
        """Create the multi-prompt router chain"""
        
        # Get expert templates
        prompt_infos = self._create_expert_templates()
        
        # Create destination chains for each expert
        destination_chains = {}
        for p_info in prompt_infos:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = ChatPromptTemplate.from_template(template=prompt_template)
            chain = LLMChain(llm=self.llm, prompt=prompt)
            destination_chains[name] = chain
        
        # Create destinations string for router
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = "\n".join(destinations)
        
        # Default chain for unmatched queries
        default_prompt = ChatPromptTemplate.from_template(
            """You are a helpful Primal TCG assistant. 
            Answer the following question to the best of your ability:
            
            {input}
            
            Response:"""
        )
        default_chain = LLMChain(llm=self.llm, prompt=default_prompt)
        
        # Router template
        MULTI_PROMPT_ROUTER_TEMPLATE = """Given a Primal TCG related question, select the most appropriate expert to answer it.
You will be given the names of available experts and their specializations.
You may also revise the original input if you think that revising it will lead to a better response.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \\ name of the expert to use or "DEFAULT"
    "next_inputs": string \\ a potentially modified version of the original input
}}}}
```

REMEMBER: "destination" must be one of the expert names listed below OR "DEFAULT".
REMEMBER: "next_inputs" can be the original input or a clarified version.

<< AVAILABLE EXPERTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT (remember to include the ```json)>>"""

        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
            destinations=destinations_str
        )
        
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )
        
        router_chain = LLMRouterChain.from_llm(self.router_llm, router_prompt)
        
        # Create the multi-prompt chain
        chain = MultiPromptChain(
            router_chain=router_chain,
            destination_chains=destination_chains,
            default_chain=default_chain,
            verbose=self.verbose
        )
        
        return chain
    
    def route_question(self, question: str) -> str:
        """Route a question to the appropriate expert"""
        return self.router_chain.run(question)
    
    def get_expert_list(self) -> str:
        """Get a formatted list of available experts"""
        experts = self._create_expert_templates()
        expert_list = "Available Primal TCG Experts:\n\n"
        for expert in experts:
            expert_list += f"• {expert['name']}: {expert['description']}\n"
        return expert_list