import os
from google.adk.agents import Agent

def save_website(folder: str, html_code: str, css_code: str = None, js_code: str = None):
    # make sure folder exists
    os.makedirs(folder, exist_ok=True)

    # Save HTML
    html_path = os.path.join(folder, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_code)

    # Save CSS if provided
    if css_code:
        css_path = os.path.join(folder, "style.css")
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_code)

    # Save JS if provided
    if js_code:
        js_path = os.path.join(folder, "script.js")
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(js_code)

    return f"✅ Website saved in folder: {folder}"


website_make_agent = Agent(
    name="website_agent",
    model="gemini-2.0-flash",
   instruction="""
You are a Website Builder Agent.  
Your tasks:  
1. Ask the user for a topic and style for the website.  
2. Generate clean, responsive HTML, CSS, and JS code.  
3. Use tools to save the generated code into files (index.html, style.css, script.js).  
4. Place all files inside the specified folder (default: 'websites/').  
5. Make sure HTML links to style.css and script.js correctly.  
6. Confirm to the user after the website is saved.  
"""
,
    tools=[save_website]
)