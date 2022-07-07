
# BiG Brother
BiG Brother is a powerful and useful tool that can be used to find IP security surveillance cameras with open ports worldwide.
To find IP cameras, the tool use the Shodan search engine API. And using specific Shodan dorks, target only video surveillance camera based on a given brands. Once an IP camera found, the script will attempt to initialize a connection to the device using associate default credentials.

![Big Brother logo](https://raw.githubusercontent.com/Nwqda/BiG-Brother/master/quests/BiG-Brother-logo.gif)

BiG Brother is not a perfect tool at the moment but provides basic functionalities to automate the search of IP cameras using Shodan API. The script can also try default credentials based on the brand found. To do this, the tool will automatically parse the HTML web page, grab the brand name and the version, and then test the default credentials associate.<br>
It is also possible to automate the search of IP cameras by targeting a specific country.

At the moment only 3 type of IP security surveillance camera brands are supported, `Sony`, `Canon` and `Panasonic`.
But I'm maybe planing to add the following brands in the near future: `Alphafinity`, `INSTAR`, `Milesight`, `Vacron` and `VideoIQ`.<br>

There is also an export functionalty that give the possibility to save the result of a research in `.csv` or `.txt` format once completed.

### Proof Of Concept
[![Video PoC BiG Brother](https://i.ibb.co/7gXHL9q/500px-youtube-social-play.png)](https://www.youtube.com/watch?v=Ns8scuSI-bE)

### Requirement
* Python 3 (Tested with Python 3.8.5)
* Shodan Account (API key)

### Installation
Clone this repository and run:
```shell
pip install -r requirements.txt
```
#### Usage
```
python3 big-brother.py
```
That's all!<br>
![Big Brother Cli](https://i.ibb.co/fD3Qrhf/big-brother-demo.png)


### List of Dorks
I am not categorizing at the moment. Instead, I am going to just the list of dorks with a description. Many of the dorks can be modified to make the search more specific or generic.

Brand          | Dork                                     | Default Credentials      | Description
-------------|-----------------------------------|--------------------------|------------------------------------------------
Panasonic |title:"network camera" | admin/12345 | Ex: WV-SW316, BB-ST165, BL-VP101...
Canon     |title:"network camera vb-" | root/camera | Ex: VB-H761LVE, VB-R13, VB-H651V...
Sony      |title:"Sony Network Camera" | admin/admin | Ex: SNC-EM602R, SNC-CX600W, SNC-EB642R...
INSTAR |title:"INSTAR Full-HD IP-Camera" | admin/instar | INSTAR?
VideoIQ |title:"VideoIQ Camera Login"  | admin/admin | VideoIQ?
Milesight |title:"Milesight Network Camera" | admin/ms1234 | Milesight?
Vacron |title:"Milesight Network Camera" | admin/admin | Vacron?
Alphafinity |title:"Alphafinity Network Camera" | admin/admin | Alphafinity?

### Note
FOR EDUCATIONAL PURPOSE ONLY. 
