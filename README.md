# Resume builder

Resume builder allows you to create resumes based on your LinkedIn profiles. All you have to do is upload your profile's PDF and on the click of a button you receive a freshly made resume.

This project utilises your specific openai API key, and it isn't saved anywhere, so it is completely private to you.

## Technical Details

On the backend the project utilises FastAPI and makes the openai calls based on the text extracted from the uploaded PDF. Following this, if no errors are encountered the openAI response is sent to the front-end as an HTML page.

The frontend is vanilla HTML and CSS based and the logical statements are handled by Javascript. Once the response is fetched successfully, the HTML resume is rendered on the same page.

test it out at: https://azaki45.github.io/Resume_builder/
