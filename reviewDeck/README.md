1. Write what you want in `slidesTemplate.md` 
2. convert this .md file to a reveal.js html presentation using pandoc
    * To do this you can use a command like
            `reveal <$1> <$2> <$3>`
    * That's IF you have added the following bash function to your ~/.bash_profile
            `reveal () {
            pandoc -t revealjs -s -o $1.html $2.md --highlight-style=tango -V revealjs-url=https://revealjs.com --metadata title="$2" -V theme="$3"
            }`

	* You could also specify you're own theme with a custom .css file. In that case the reveal function would be 

		`reveal () {
pandoc -t revealjs -s -o $1.html $2.md --highlight-style=tango -V revealjs-url=https://revealjs.com --metadata title="$2" --include-in-header=/path/to/slides.css"}`

3. Now you must navigate to the folder where you want your .html slides to be created
4. Then call `reveal mySlides lecture-template <theme>`
    - where theme could be any of [beige, black, blood, league, moon,
night, serif, simple, sky, solarized, white]

5. You should see mySlides.html created in that folder


