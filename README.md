# DomainModelingPrompter
Domain Model Prompter (DMP) extracts domain/ conceptual model (classes/concepts and relationships) from user stories. It is implemented using Large Language Model (LLM) -gpt-3.5-turbo and prompt chaining. 

# Input
Set of well formed user stories having role, funciton and benefit part written in the format: “As a <role> I want to <feature>, so that <benefit>. Benefit part is optional.

# Output
Graphical domain model.

# DataSets used for evaluation

<b>Restaurant Management System (RMS): </b>RMS.txt<br>
<b>Order Processing System (OPS): </b>OPS.txt<br>
<b>Camping System (CP): </b>CP.txt<br>

# Results
<b>Results reported in the paper are summarized in the files: </b>Results_DMP_RMS.xlsx, Results_DMP_OPS.xlsx, Results_DMP_CP.xlsx<br>
<b>Results of comparison of DMP with existing tool Visual Narrator (VN) are presented in the files: </b>Results_Comparison_VN_DMP-RMS.xlsx, Results_Comparison_VN_DMP-OPS.xlsx, Results_Comparison_VN_DMP-CP.xlsx<br>
<b>Results for the Planning Poker data set are presented in the file: </b>Results_Dataset2.xlsx<br>

# Implementation
Domain Model Prompter (DMP), the tool developed to extract classes and relationships from user stories, was implemented according to the proposed method using LLMs and prompt chaining. 
The tool is implemented in ‘Python’ (version: 3.9.13) and made use of the ‘OpenAI’ Python client in combination with the ‘gpt-3.5-turbo’ model for generating responses. 
The ‘openai’ library (version: 1.10.0) manages the interaction with the language model. 
For chat completion, the key parameters temperature, maximum token length, top-p, frequency penalty, and presence penalty are tuned to values 0, 2048, 1, 0, and 0 respectively.
Out of which the last three are kept at their default values. The temperature is tweaked to value 0 from 1 so as to minimize the variation between the responses generated by the model. The token limit is increased to 2048 from the default 256 so as to get longer response involving many tokens. 
The tool has chat like interface where domain model is constructed based on the interaction taking place between the domain modeling assistant and the domain modeler/ user. 
The tool uses ‘panel’ library (version: 1.3.8) for web based chat interface. We use ‘graphviz’ library (version: 0.20.1) for visualizing and representing the extracted domain models in graphical form. 
The use of ‘json’ library (version: 2.0.9) facilitates handling and parsing of data generated by the model in JSON format.
