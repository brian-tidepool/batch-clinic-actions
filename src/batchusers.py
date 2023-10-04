from healthkit_precise import *
import os


runs = os.environ.get("INPUT_NUM")
prefix = os.environ.get("PREFIX")
def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))


days=30 #since upload
goal_num = 1 #cgm use
percent_num=0.3 # percent in verylow
env = 'https://qa1.development.tidepool.org' #environment

for i in range(runs):
    #prefix=random_char(4)
    prefix = 'fvn'
    username='brian+'+prefix+str(i)+'@tidepool.org'
    run(env,username,days,goal_num,percent_num)

print(f"::set-output name=result::{'done'}")