# ETA-on-DoH
Evaluation of User Privacy using Encrypted Traffic Analysis on DoH traffic of websites

PROBLEM STATEMENT

Our goal is to find out whether it is possible to fingerprint and identify webpages from encrypted
DNS. This information is of interest to almost all of us today. There are many ways in which people
can divulge their personal information, for instance by use of social media and by sending bank and
credit card information to various websites. Moreover, directly observed behavior, such as browsing
logs, search queries can be automatically processed to infer potentially more intrusive details about
an individual, such as political and religious views, race, intelligence, and personality. Hence,
internet privacy is a concern for every internet user irrespective of their activity on the internet.
Encrypted DNS, namely, DNS-over-HTTPS and DNS-over TLS guards user privacy by hiding
DNS resoltuions from passive adversaries. However, the way DNS works, we can never have end-
to-end encryption for browser to server, without making it known to intermediate servers. In each
DNS query, the full hostname is sent to all the intermediate DNS servers, though it is of real interest
to only your website's name server. A solution to this is DNS query name minimization, but that too
doesn't give you complete anonymity, but certianly reduces the amount of data you give away. And
with encrypted DNS the resolutions being hidden, we try to find out if we can infer websites from
other channels avaible to us inspite of encryption. In this work, we raise the question "Does
encrypted DNS provide the same extent of privacy as it claims to offer?". For this we have created a 
dataset, extracted DNS sequences and checked if we can predict user activities.

METHODOLOGY

To evaluate the extent of online privacy offered by encrypted DNS we chose to work with DNS
sequences, since it relies on statistical features and can be extracted inspite of encrypted messages.
For our experiment, we firstly configure Mozilla Firefox on Ubuntu 18.04 LTS to enable DNS-over-
HTTPS, since that is one of the platforms which has implemented DoH widely. We then design a
web crawler through which we extract all the links present in a website, namely,
'www.wireshark.org' , and then use those links to create our dataset. For every link, the webpage is
loaded in Mozilla firefox, packets are captured and then the next webpage is loaded. These packets
are then decrypted using the decryption key and DNS sequences are extracted from it. From this we
get an idea about the size range under which dns packets fall, and use it for our next phase-
prediction.
1. Web Crawler:
We designed a web crawler using the "BeautifulSoup" module in python, which basically is a
bot that extracts all the links present in the website we provided. We also used the modules
"url" and "re", to filter valid internal urls only. All the extracted links were written to an
external text file. We stopped extracting urls once we had thousand urls, since that would be
enough to conduct our experiment. 
2. Profiling:
For the packet capture we first created a log file which will contain the decryption key.
Along with it we wrote a bash script where it first clears the browser history, cache and
cookies and then starts the capture. It loads the webpage in a browser and once done it kills
the browser and stops the capture. This bash script is included in a python script which
takes each url from the text file containing all links extracted from the website, and runs the
script to capture packets from that link. To create a diverse dataset we have loaded the
web page of each url 10 times, that is each of those thousand urls where loaded ten times and
a total of ten thousand pcap files were created and the decryption key was also stored in a
file which we would require while extracting the DNS sequences. The links to the dataset created after execution can be found in the README file of the signature extraction process.

ALGORITHM FOR PROFILING

STEP 1:

The first step of profiling is taking input parameters. We first read all the parameters from
command line call, and store them in their respective variables, so that we can use the
information later in the program. Like, the file name containing all the links extracted
using web crawler, is taken as input through the parameter 'listfile' is stored in the listfile
variable.

STEP 2:

In case the user gives wrong arguments as input, we have also defined an error function,
that would let the user know which argument is used for what purpose, so that the user can
identify and rectify the mistake. This function simply prints the purpose of each arguement
and exits.
The input parameters and their functions are as follows--
-whole{ /whole/ }: 1 =profile all web pages in the website, 0 =profile a specific set of pages
-webdir{ /webdir/ }: directory containing website map (output of navigation.py)
-listfile{ /listfile/ }: path to file containing list of web pages to profile (for whole = 0)
-uplevel{ /uplevel/ }: till what parent level profiling has to be done (for whole=0) [default: 0]
-downlevel { /downlevel/ }: till what child level profiling has to be done (for whole=0)
[default: 0]

STEP 3:

We make sure that the users have given correct inputs of all the parameters present,
especially 'listfile' since without this we won't have access to the file containing all the links and
consequently won't be able to collect traffic samples.

STEP 4:

Next we start collecting traffic samples from the URLS present in the file. For this we open
the input file, take each URL and first write it to a file called 'statistics', so that at the end of the
process we can have a list of all those urls for which we have successfully collected traffic
samples. Also, in case of bugs, this file helps us in debugging.

STEP 5:

To collect traffic samples we call our bash script for each url, using the subprocess module.
This script first clears browser history along with cache and cookies, and then starts the
packet capture with tshark command. Once the webpage is loaded in the browser(here,
Mozilla Firefox) it kills the browser and stops the packet capture. All the pcaps generated
are stored in the same directory with url numbers, and each url is loaded ten times. Hence,
pcaps are named as 1_0.raw, 1_1. raw and so on.

3. Extracting DNS Sequences:
Once ten thousand pcap files were created along with the decryption key, we wrote a python
script which firstly filtered the encrypted DNS packets with the help of tshark, using the
filter 'tcp.dstport==443 && dns' ,which filters all the response DoH packets. Next, we
decrypt these packets using the decryption key we retrieved while creating the dataset and
then stored the record length, i.e, the message size of each dns packet, of each url in a list
and finally stored it in a folder. That implies the folder had thousand files numbered from 1
to 1000, and each file had 10 DNS sequences for the url, since each url was loaded ten times
and packets were captured.

4. Finding the common sequence:
Now, we decided to cut short the concept of ten dns sequences for each url and instead have
one for each. For this we found out the longest common subsequence from all the ten dns
sequences for each url , and stored it in a file. If there are more than one sequence with the
maximum length, we store all of them. Since we worked with longest common subsequence
it means that the url from which we captured packets, will have this sequence as a
subsequence most of the times.

5. DNS size range:
During this entire process, the adversary will have access to the decryption key and hence
could filter the DNS packets from all the encrypted packets. But during the prediction phase it
will not have access to the key. Hence we write a python script that would extract the
final set of sizes of the DNS packets, so that when we can't decrypt the packets we can know
which packets are DNS packets by looking at their packet sizes. For this we simply take every
DNS sequence present in the common sequence file and find the distinct packet sizes. We
chose this method, since inspite of encryption the packet sizes, an application layer
information, is always available to us.

6. Prediction algorithm:
We now had with us the file which contained dns sequence for each url and the url list. To
predict a website, a pcap is provided as input to the sample code we wrote for the prediction
algorithm. Our algorithm extracts the dns sequence from the given input pcap, using the dns
size range we had from our signature extraction process, and then performs two checks hat
is finds the longest common subsequence and then the longest common subarray between
the extracted dns sequence from the input pcap and each url from the file, to predict the
webpage that the user was browsing.

ALGORITHM FOR PREDICTION

STEP 1:

The first step to predict the url is to extract the dns sequence from the given pcap. But
since it is encrypted and we don't have access to the decrpytion key, we would first
need to filter the DNS packets. For this we make use of the DNS size range we had
extracted earlier. Using this information, we filter those packets whose packet sizes fall
under this range and conclude that these are dns packets. From these packets, we form a
DNS sequences using their sizes ('tls.record.length'), which is an application layer
information and hence available to us inspite of encryption. Therefore, we now have the
DNS sequence of the given input pcap file.

STEP 2:

Once we have the DNS sequence of our input pcap file, we then proceed to the first
check that is the longest common subsequence. For this, we wrote a function
'check_exists()' that took two parameters. One is the input dns sequence and the other is the
dns sequence of each url. So, we passed one DNS sequecne of one url each time
from the file along with the input dns sequence to the function check_exists(). This function
checks whether the dns sequence from the file (for each url) is present as a subsequence in
the input dns sequence or not. Based on the results it returns a boolean value, either True or
False.

STEP 3:

If the function returns True we add the url number of the url which is present as a
subsequence in the input dns sequence, into a set. If it returns False, we continue our check
on other urls. We use a set here since one url may have multiple dns sequences, and all of
them might be a subsequence of the input dns sequence. To avoid duplicate url numbers and
unecessary checks we add it to the set.

STEP 4:

After the first check the number of predicted urls are large in number and hence we do
another check by finding the longest common subarray. Here the function "isSubArray()" is
used which takes four parameters: the input dns sequence, each dns sequence from the file,
size of the input dns sequence and size of each dns sequence from the file. This function
again returns a boolean value either True-- if each dns sequence is present as a subarray in
the input dns sequence or False-- if not present.

STEP 5:

At this point we create a dictionary. Whose key-value pair is the url number-length of the
dns sequence. If the “isSubArray()” function returns True it we store it's url number as the key
and the length of the dns sequence as it's corresponding value. If it returns False, we simply
continue our checks on other urls.

STEP 6:

While storing the values in the dictionary, we simultaneously also find the maximum length
out of all all of the dns sequence lengths that we stored. This indicates that out of all the urls
having a common subarray with the dns sequence extracted from the given input pcap, the
one having the maximum length matches the most with the input pcap's dns sequence and
hence has the highest probability to be the url that the user was browsing.

STEP 7:

Sine there can be more than one url having maximum length, we store all the url numbers in a
set which have that length. We again use a set here to avoid repetative url numbers.

STEP 8:

We finally open our file containing the names of all the urls, and then print those urls which
have their url numbers present in the set. These urls are the predicted urls. Most of the times
it is just one correctly predicted url, but sometimes it is more than one too.

EXPERIMENTAL OBSERVATIONS 

The file that conatined dns sequences for each url had remarkably a lot of sequences in common, which portrays that if the webpage which is loaded 10 times tends to have a lot of common sequences, then our prediction algorithm which is designed to work on the longest common subsequence of these dns sequences would work fine. However, our prediction algorithm which is in a very initial state sometimes predicts more than one url. More time is required to make this algorithm efficient, and we believe once we have a strong prediction algorithm we can successfully predict the url which was provided to us, since we already can predict the url most of the time. 

CONCLUSION 

Our experimental observations have shown that we can successfully fingerprint and identify webpages, inspite of encryption. DNS-over-HTTPS hides the DNS resolution, but we still can infer the user's activity using other information which is easily availabe to us, that is, message sizes of DNS response packets. The prediction algorithm designed by us is not completely efficient and we would require time to work on it to produce 100% accurate results. However, with our present work we still can conclude that internet privacy is at threat even with the implementation of encrypted dns. 
