# 💥 ATLAS4teachers Web App 💥
> [Click here to see the app!](https://atlas4teachers.app.cern.ch)

This analysis web app was created as introductory material to the world of physics analyses. It was initially used in a high school teachers workshop [in Mexico](https://indico.cern.ch/event/1466744/overview) and [Colombia](https://indico.cern.ch/event/1483118/overview).

The web app is currently available in English and Spanish. If you are interested in translating the app, you can find instructions below.

## 🖥️ About the app
The app is written in Python using the Streamlit library. It is hosted on the OKD service from CERN. 

It includes the following sections:
1. **Foundations of Particle Physics**: Basics about particles, the Standard Model and beyond.
2. **Experimental Particle Physics**: Introduction to the LHC, detectors and the ATLAS experiment.
3. **Hands-on Analysis**: Identifying the Z boson via its dileptonic decay and the Higgs boson through the ZZ channel.
4. **Introduction to Python**: Material on Python basics and histogramming.
5. **Classroom Toolkit**: Extra material in other formats like video, cheat sheets, fact sheets, etc.

## 📝 Translating the app
Since most of the documentation in the app is in markdown format, translating it should be fairly easy.

### 1. Copy the `english` folder
Inside the `docs` folder you will find all the information displayed in the app. For instance, all the information in the app in English is inside the `english` folder. 

To add a new language, make a copy of the `english` folder, also inside the `docs` folder, and rename it with the name of the language you are translating to.

If you are adding a language "newlanguage", you should see something like this inside `docs`:
```
docs
|_ english
|_ spanish
|_ ...
|_ newlanguage
```
### 2. Add the new language as an option to the app
To add the new language to the app go to the `app.py` file and look for this line (L53):
```
# Dropdown for language selection
    language = st.selectbox("Select Language", ["English", "Spanish"])
```
Add the new language as follows:
```
# Dropdown for language selection
    language = st.selectbox("Select Language", ["English", "Spanish", "Newlanguage"])
```
The name has to match the name of the folder you copied in `docs` but the first letter should be in caps.

### 3. Run the app locally
It's recommended to run the app locally to see changes live. For this, you need to create an enviroment with the packages listed in `requirements.txt`. If you are using conda, this can be achieved by:
```
conda create --name myenv python=3.11
conda activate myenv
pip install -r requirements.txt
```
Then you can run the app using the `streamlit run` command:
```
streamlit run app.py
```
### 4. Translate all the files
Now you are set to start translating the app. The new language should be an option in the first screen of the local version of the app at this point.

Go through each folder and translate the files that are inside the `newlanguage` folder. Once you save the changes, you should see the change in app you are running locally

### Notes about the markdown files
There are some parts of the text that tell the app how to show things, and you should be aware to avoid changing them by mistake:
#### Tags
Sometimes you will find text between tags like these: ```> [!NOTE] ... > [!END]```. Do not translate the words in the tags (NOTE and END, for this example), and keep the tags above and below the text. The text in between should be translated.
#### Images
The images are embeded from the text, so you will find lines like this in the middle of the markdown `![Image 1: The ATLAS detector and its parts.](images/ATLAS_detector.png)`. Most images are good for every language, so you only should change the text that says "Image 1: The ATLAS detector and its parts." However, there are some images that have text, for example for the parts of the ATLAS detector. If you find an image that works better for the language you are translating to, add it to the `images` folder, and just change the name of the image on the path (in this case `images/ATLAS_detector.png` -> `images/your_image.png`)
#### Code 
The markdowns for the python section include the code that is shown in the app. The comments for the code should be translated, but nothing else. For example you can find something like this:
    ```python
    print(4**(1/2)) # Use fractional powers to calculate roots
    ```
    And the idea would be to translate "Use fractional powers to calculate roots"
#### JSON files for the analyses
The `analysis` folder include JSON files. Only the values should be translated, not the keys. For example:
```
"lepton_pt": {
"selectbox_label": "Now, let's make the cut:",
"apply_button": "Cut on leptons p$_T$"
}
```
Here you should translate: "Now, let's make the cut:", "Cut on leptons p$_T$".

## 📊 Running the analyses
The plots for the analyses included in the app were obtained using the `analysis.py` file found inside the `scripts` folder. 

The script can be use with the following parameters:
```
usage: analysis.py [-h] [-l LUMIS [LUMIS ...]] [-n NLEP [NLEP ...]] [-f FLAVLEP [FLAVLEP ...]] [-c CHARLEP [CHARLEP ...]]

Run analysis for teachers app with ATLAS Open Data

options:
  -h, --help            show this help message and exit
  -l LUMIS [LUMIS ...], --lumis LUMIS [LUMIS ...]
                        List of Integrated luminosities for the analysis [Default: 36]
  -n NLEP [NLEP ...], --nlep NLEP [NLEP ...]
                        List of Number of leptons for the analysis [Default: 2]
  -f FLAVLEP [FLAVLEP ...], --flavlep FLAVLEP [FLAVLEP ...]
                        List of Flavors for lepton pairs. Options: same, different [Default: same]
  -c CHARLEP [CHARLEP ...], --charlep CHARLEP [CHARLEP ...]
                        List of Charges for lepton pairs. Options: same, opposite [Default: opposite]
```
For example, to find the Higgs in the ZZ channel with 36 1/fb:
```
python analysis.py -l [36], -n [4], -f ['same'], -c ['opposite']
```
If multiple options are listed in any of the input parameter, it will run through all the combinations of parameters given. 
