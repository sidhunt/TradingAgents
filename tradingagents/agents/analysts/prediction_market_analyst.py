"""
Prediction Market Analyst Agent
=============================

This agent specializes in analyzing prediction markets, particularly from Polymarket.
It evaluates market probabilities, volume trends, and sentiment to provide trading insights.

Author: TradingAgents Framework
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_prediction_market_analyst(llm, toolkit):
    """
    Create a prediction market analyst agent that specializes in analyzing
    prediction markets and binary outcome events.
    """

    def prediction_market_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state.get("company_of_interest", "")
        
        # For prediction markets, we might be looking at events rather than companies
        market_category = state.get("market_category", "crypto")
        
        # Tools for prediction market analysis
        tools = [
            toolkit.get_polymarket_events,
            toolkit.get_polymarket_market_analysis,
            toolkit.get_trending_prediction_markets,
        ]

        system_message = """You are a specialized prediction market analyst with expertise in analyzing binary outcome markets, particularly on Polymarket. Your role is to evaluate prediction market opportunities by analyzing:

**Core Analysis Areas:**
1. **Market Probabilities**: Assess whether current market prices accurately reflect true probabilities
2. **Volume & Liquidity**: Evaluate trading activity and market depth
3. **Event Fundamentals**: Analyze the underlying events and their likelihood
4. **Market Sentiment**: Gauge crowd wisdom vs. expert opinions
5. **Risk Assessment**: Identify potential biases and market inefficiencies

**Prediction Market Types:**
- **Political Markets**: Elections, policy outcomes, regulatory decisions
- **Economic Markets**: Fed rates, GDP, inflation, employment data  
- **Crypto Markets**: Price predictions, protocol upgrades, adoption metrics
- **Sports Markets**: Game outcomes, season results, performance metrics
- **Technology Markets**: Product launches, company milestones, adoption rates

**Key Metrics to Analyze:**
- Current probability (price) vs. your assessed probability
- Volume trends and liquidity depth
- Time to resolution and decay effects
- Historical accuracy of similar markets
- Information asymmetries and insider knowledge
- Correlation with traditional financial markets

**Trading Considerations:**
- Binary outcomes (0 or 1) create different risk profiles than traditional assets
- Markets can be inefficient due to limited participation
- Emotional biases often affect political and sports markets
- Resolution risk and platform risk factors
- Liquidity constraints for position sizing

**Your Analysis Should Include:**
1. **Event Assessment**: What is the true probability of the outcome?
2. **Market Efficiency**: Is the current price accurate or mispriced?
3. **Risk Factors**: What could invalidate your analysis?
4. **Trading Strategy**: How to position and manage risk
5. **Timing**: When to enter and exit positions

Focus on providing actionable insights that help traders identify opportunities where market prices diverge from true probabilities. Always consider the unique characteristics of prediction markets compared to traditional financial instruments.

Make sure to use the available tools to gather current market data and trends before making your analysis."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
            ("user", "Please analyze the current prediction market landscape for {market_category} markets on {current_date}. "
                     "Focus on identifying potential trading opportunities where market prices may not accurately reflect true probabilities. "
                     "Provide specific recommendations with risk assessments.")
        ])

        bound = prompt | llm.bind_tools(tools)
        
        # Get the current messages from state
        messages = state.get("messages", [])
        
        # Add the analysis request
        analysis_request = {
            "market_category": market_category,
            "current_date": current_date,
            "ticker": ticker  # This might be relevant for crypto/stock-related prediction markets
        }
        
        response = bound.invoke({
            "messages": messages,
            "market_category": market_category,
            "current_date": current_date
        })
        
        # If the response contains tool calls, execute them
        if response.tool_calls:
            tool_results = []
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                try:
                    if tool_name == "get_polymarket_events":
                        result = toolkit.get_polymarket_events(**tool_args)
                    elif tool_name == "get_polymarket_market_analysis":
                        result = toolkit.get_polymarket_market_analysis(**tool_args)
                    elif tool_name == "get_trending_prediction_markets":
                        result = toolkit.get_trending_prediction_markets(**tool_args)
                    else:
                        result = f"Unknown tool: {tool_name}"
                    
                    tool_results.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": result
                    })
                except Exception as e:
                    tool_results.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": f"Error: {str(e)}"
                    })
            
            # Create follow-up analysis with tool results
            analysis_prompt = f"""
Based on the prediction market data gathered, provide a comprehensive analysis focusing on:

1. **Market Opportunities**: Identify specific markets where prices may be mispriced
2. **Probability Assessment**: Your estimated true probabilities vs. market prices
3. **Volume Analysis**: Which markets have sufficient liquidity for trading
4. **Risk Factors**: Key risks that could affect these markets
5. **Trading Recommendations**: Specific positions to consider with reasoning

Tool Results:
{json.dumps(tool_results, indent=2)}

Provide actionable insights for prediction market trading opportunities.
"""
            
            # Get final analysis
            final_response = llm.invoke([
                {"role": "system", "content": system_message},
                {"role": "user", "content": analysis_prompt}
            ])
            
            analysis_content = final_response.content
        else:
            analysis_content = response.content
        
        # Structure the response
        prediction_market_analysis = {
            "analyst_type": "prediction_market_analyst",
            "analysis_date": current_date,
            "market_category": market_category,
            "analysis": analysis_content,
            "tools_used": [tool_call["name"] for tool_call in response.tool_calls] if response.tool_calls else [],
            "confidence_level": "medium",  # This could be derived from the analysis
            "timestamp": time.time()
        }
        
        # Add to messages
        new_messages = messages + [
            {
                "role": "assistant",
                "content": f"**Prediction Market Analysis - {market_category.title()}**\n\n{analysis_content}",
                "metadata": {
                    "analyst": "prediction_market_analyst",
                    "category": market_category,
                    "analysis_date": current_date
                }
            }
        ]
        
        return {
            "messages": new_messages,
            "prediction_market_analysis": prediction_market_analysis
        }
    
    return prediction_market_analyst_node