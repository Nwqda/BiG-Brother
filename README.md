
# BiG Brother
BiG Brother is a powerful and useful tool that can be used to find video surveillance cameras with open ports worldwide.
To find this, the tool use Shodan search engine with its API. And with the help of the Shodan dorks, target only specific video surveillance camera brands of your choice. Once a camera detected, BiG Brother will attempt to initialize a connection to it using associate default credentials.

![Big Brother logo](https://s6.gifyu.com/images/BiG-Brother-logo.gif)

BiG Brother is not a perfect tool at the moment but provides basic functionalities to automate the search of video surveillance cameras with open port on Shodan and try to connect to it with using default credential. To do that, the tool will automatically detect what kind of video surveillance cameras is it (brand and model) and test the default credentials associate. It's also possible to automate the search of cameras by targeting a specific country.

At the moment only 3 video surveillance camera brands are supported, `Sony`, `Canon` and `Panasonic`.
I plan to add the following brands in the coming weeks: `Alphafinity`, `INSTAR`, `Milesight`, `Vacron` and `VideoIQ`.
There is also the possibility to save and export the result of the research in `.csv` or `.txt` once completed.

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
Then let yourself be guided!
![Big Brother Cli](https://i.ibb.co/fD3Qrhf/big-brother-demo.png)

### Contribution
Please consider contributing dorks that can reveal cameras on Shodan.

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
