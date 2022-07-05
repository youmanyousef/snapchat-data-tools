# snapchat-data-tools
Helpful tools I made to make sense of the data you can download from Snapchat

I hope to add more tools in the future, and please do write to me and help me out!
## Snapchat Memories Downloader
This requires Python 3.x and the python module [requests](https://requests.readthedocs.io/en/latest/). If you like, you can install an executable from the Releases tab and skip installing these prerequisites. 

To download all of your memories, you have to request to get your data from Snapchat [here.](https://accounts.snapchat.com/accounts/downloadmydata)

Then, extract the zip archive, and navigate to JSON/memories_history.json. Copy/Move this to where you saved the downloader.

Finally, run the command with this usage. (The last option for destination is optional - default is a directory named "memories")

``` bash
$ downloader.py memories_history.json "./destination"
```
