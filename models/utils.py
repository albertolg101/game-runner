def extract_content(output):
    return str(output.choices[0].message.content).replace("```", "")