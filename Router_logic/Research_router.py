import os

from semantic_router.encoders import OpenAIEncoder
from semantic_router import Route, RouteLayer

os.environ["OPENAI_MODEL_NAME"] = "text-embedding-3-large"

# Define the system notes for each type of route as constants

GENERAL_INFORMATION = """SYSTEM_NOTES: The user is initiating an inquiry into a topic, likely with minimal prior 
understanding. Your response should serve as an introductory guide, offering a concise yet comprehensive overview. 
Prioritize clarity and simplicity, avoiding technical jargon unless defined. Highlight key concepts and facts that 
form the backbone of the topic, ensuring they are directly relevant to the user's query. Aim to pique the user's 
interest with engaging content that invites further exploration. Your goal is to provide a foundational understanding 
that empowers the user to pursue more in-depth knowledge if they choose."""

SPECIFIC_DETAIL = """SYSTEM_NOTES: The user has requested information that hinges on specific details or facets of a 
broader topic. Your response should be rich with exactness and precision. Ensure the accuracy of the information 
provided, citing data or statistics to substantiate the claims when relevant. Place the detail within its larger 
context to elucidate its relevance and impact on the topic as a whole. If the detail involves technical terms or 
complex concepts, provide clear explanations to facilitate comprehension. The response should not only inform but 
also deepen the user's understanding of the particular aspect in question."""

COMPARATIVE_INFORMATION = """SYSTEM_NOTES: The user has posed a query that necessitates a comparative analysis. 
Approach the response with a critical and analytical mindset, examining both similarities and differences. Ensure the 
comparison is balanced, offering an impartial assessment that avoids bias. Provide evidence-based conclusions, 
drawing from data, studies, or expert opinions to substantiate your analysis. Where possible, distill the information 
into a conclusive summary or recommendation, aiding the user in decision-making or understanding the comparative 
significance of each element involved. Your response should not only contrast the entities but also enlighten the 
user on the broader implications of these comparisons."""

HISTORICAL_INFORMATION = """SYSTEM_NOTES: The user seeks insight into the historical trajectory of a topic. Construct 
a response that outlines the topic's evolution in a clear chronological order. Emphasize pivotal milestones, 
discoveries, or figures that have significantly impacted the topic's direction. Explain the causal relationships 
between historical events and their outcomes, shedding light on how past developments have laid the groundwork for 
the present. Where relevant, bridge the historical narrative to modern-day implications, demonstrating the topic's 
ongoing significance or legacy. Your response should not only recount history but also provide a lens through which 
the user can understand the topic's current and potential future state."""

PROCEDURAL_INFORMATION = """SYSTEM_NOTES: The user is seeking guidance on how to execute a task or understand a 
procedure. Your response should serve as a practical manual, structured as a series of clear, actionable steps. Begin 
with a brief introduction to the task at hand, then proceed with a sequential list of instructions, ensuring each 
step is necessary and contributes to the completion of the task. Be comprehensive without overwhelming the user, 
and maintain a level of simplicity in your language to accommodate a broad audience. Include tips or best practices 
where applicable, and consider providing warnings for common mistakes or misconceptions. The objective is to empower 
the user to perform the task independently and successfully with the information you provide."""

PREDICTIVE_INFORMATION = """SYSTEM_NOTES: The user is looking forward to grasping potential developments within a 
given topic. Frame your response with a forward-looking perspective, synthesizing current trends and data to outline 
possible future scenarios. Incorporate insights from authoritative sources and experts to lend credibility to your 
predictions. Present a spectrum of outcomes where applicable, from the most likely to less probable, to capture the 
range of possibilities. Emphasize the speculative nature of predictions and clearly state any assumptions underlying 
your forecast. The aim is to provide the user with a thoughtful, informed conjecture that sparks consideration and 
prepares them for what might lie ahead."""

PROBLEM_SOLVING = """SYSTEM_NOTES: The user is facing a challenge and seeks a solution or guidance to overcome it. 
Approach your response with empathy and a focus on clarity. Offer practical, step-by-step advice tailored to the 
user's specific problem, ensuring that each step is actionable and comprehensible. Anticipate potential obstacles or 
common mistakes related to the problem and provide strategies to navigate or avoid them. Where appropriate, 
supplement your advice with examples, analogies, or additional resources that the user might find helpful. The goal 
is to empower the user with the knowledge and confidence to tackle their issue effectively, fostering a sense of 
support and understanding."""

# Map the system notes to the route names
system_notes_mapping = {
    'general_information': GENERAL_INFORMATION,
    'specific_detail': SPECIFIC_DETAIL,
    'comparative_information': COMPARATIVE_INFORMATION,
    'historical_information': HISTORICAL_INFORMATION,
    'procedural_information': PROCEDURAL_INFORMATION,
    'predictive_information': PREDICTIVE_INFORMATION,
    'problem_solving': PROBLEM_SOLVING
}


class Research_route_manager:
    def __init__(self):
        self.route_layer = None
        self.routes = None
        self.encoder = OpenAIEncoder(name="text-embedding-3-large", score_threshold=0.3)  # Ensure your API key is set appropriately
        self.setup_routes()

    def setup_routes(self):

        # 1. Specific Detail Requests
        specific_detail_route = Route(
            name="specific",
            utterances=[
                "What are the main causes of {specific consept} in {topic}?",
                "How does {specifics} affect {topic}?",
                "I need comprehensive information about {specific} in {topic}.",
                "Can you break down the {specific} of {topic} for me?"
            ]
        )

        # 2. Comparative Information Requests
        comparative_info_route = Route(
            name="comparative_information",
            utterances=[
                "Compare {topic1} and {topic2} for me.",
                "What are the differences between {topic1} and {topic2}?",
                "How is {topic1} similar to {topic2}?",
                "I'm trying to understand how {topic1} and {topic2} relate to each other."
            ]
        )

        # 3. Historical Information or Evolution
        historical_info_route = Route(
            name="historical_information",
            utterances=[
                "What is the history of {topic}?",
                "How has {topic} evolved over time?",
                "Trace the development of {topic}.",
                "I want to understand the historical background of {topic}."
            ]
        )

        # 4. Procedural or How-To Information
        procedural_info_route = Route(
            name="procedural_information",
            utterances=[
                "How do I {perform a task} in {topic}?",
                "What are the steps for {performing a task} in {topic}?",
                "Can you guide me through the process of {task} in {topic}?",
                "I need a walkthrough on {task} in {topic}."
            ]
        )

        # 5. Predictive or Future-Oriented Information
        predictive_info_route = Route(
            name="predictive_information",
            utterances=[
                "What are the future trends in {topic}?",
                "How is {topic} expected to change in the future?",
                "Predict the future of {topic}.",
                "I'm curious about what's next for {topic}."
            ]
        )

        # 6. Problem-Solving or Troubleshooting Information
        problem_solving_route = Route(
            name="problem_solving",
            utterances=[
                "How do I solve {problem} in {topic}?",
                "I'm having trouble with {problem} in {topic}.",
                "What are common solutions for {problem} in {topic}?",
                "Guide me through troubleshooting {problem} in {topic}."
            ]
        )

        # Initialize the RouteLayer with the defined routes
        self.routes = [
            specific_detail_route,
            comparative_info_route,
            historical_info_route,
            procedural_info_route,
            predictive_info_route,
            problem_solving_route
        ]

        # Add more routes if needed
        self.route_layer = RouteLayer(encoder=self.encoder, routes=self.routes)


def create_full_prompt(question_analyzed, research_route_manager):
    # Analyze the question to determine the route
    route_choice = research_route_manager.route_layer(question_analyzed).name
    print(f"Route chosen: {route_choice}")

    # Fetch the system notes for the chosen route, default to GENERAL_INFORMATION if not found
    system_notes = system_notes_mapping.get(route_choice, GENERAL_INFORMATION)

    # Construct the full prompt
    full_prompt = f"Question: {question_analyzed}\n\n{system_notes}\n\nResponse:"

    return full_prompt


if __name__ == "__main__":
    Prompt_manager = Research_route_manager()
    # Sample question for testing
    sample_question = "I have a problem learning python. can you guide this to me"
    # Create a prompt using the sample question and the Research_route_manager instance
    prompt = create_full_prompt(sample_question, Prompt_manager)
    # Print the generated prompt
    print(prompt)
