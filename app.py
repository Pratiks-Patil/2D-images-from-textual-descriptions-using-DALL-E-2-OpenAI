from flask import Flask, render_template, request
import openai
# import spacy
import en_core_web_sm
import time

# Load the English language model for spaCy
nlp = en_core_web_sm.load()

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Get the textual description from the form data
    description = request.form['description']
    
    # Split the input text into sentences using spaCy
    doc = nlp(description)
    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 0]

    # Generate an image for each sentence using the OpenAI Image API
    image_urls = []
    for sentence in sentences:
        # Perform natural language preprocessing on the sentence using spaCy
        doc = nlp(sentence)
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ', 'VERB'] or token.ent_type_ in ['PERSON', 'ORG', 'GPE']]
        prompt = ', '.join(keywords)

        while True:
            try:
                # Generate an image using the OpenAI Image API
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512"
                )
                image_url = response['data'][0]['url']
                image_urls.append(image_url)
                break
            except openai.error.RateLimitError:
                print("API rate limit exceeded. Waiting for 1 minute...")
                time.sleep(60)
    
    # Display the generated images on the web page
    return render_template('result.html', image_urls=image_urls)

if __name__ == '__main__':
    app.run(debug=True)