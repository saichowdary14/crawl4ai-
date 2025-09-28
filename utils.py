def extract_year_and_state_from_prompt(prompt: str, year_options: list, state_options: list):
    prompt_lower = prompt.lower()

    matched_year = None
    for year in year_options:
        if year.lower() in prompt_lower:
            matched_year = year
            break

    matched_state = None
    for state in state_options:
        if state.lower() in prompt_lower:
            matched_state = state
            break

    return matched_year, matched_state

