import pickle
from math import sqrt
from PIL import Image, ImageDraw
from scale2D import *


def getHeight(clust):
    #Is this an endpoint ? Then the height is just 1
    if clust.left == None and clust.right == None: return 1

    #Otherwise the height is the sum of the heights of each branch
    return getHeight(clust.left) + getHeight(clust.right)


def getDepth(clust):
    #The distance of an endpoint is 0.0
    if clust.left == None and clust.right == None: return 0

    #The distance of a branch is the greater of its two sides plus its own distance
    return max(getDepth(clust.left),getDepth(clust.right)) + clust.distance


def drawDendogram(clust,labels,jpeg='twitterClusters.jpg'):
    #height and width
    h = getHeight(clust)*20
    w = 1200
    depth = getDepth(clust)

    #width is fixed, so scale distances accordingly
    scaling = float(w-150)/depth

    #Create a new image with a white background
    img = Image.new("RGB", (w,h) , (255,255,255))
    draw = ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    # Draw the first node
    drawNode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')


def drawNode(draw,clust,x,y,scaling,labels):
    if clust.id < 0:
        h1 = getHeight(clust.left)*20
        h2 = getHeight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2
        # Line length
        ll=clust.distance*scaling
        # Vertical line from this cluster to children
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

        # Horizontal line to left item
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))

        # Horizontal line to right item
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

        # Call the function to draw the left and right nodes
        drawNode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
        drawNode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x+5,y-7),labels[clust.id].encode('utf-8'),(0,0,0))


#Pearson distance index
def pearson(v1,v2):
    v1 = [item[1] for item in v1]
    v2 = [item[1] for item in v2]

    #Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    #Sums of the squares
    sum1Sq = sum([pow(v,2) for v in v1])
    sum2Sq = sum([pow(v,2) for v in v2])

    #Sum of the products
    pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

    #Calculate r (Pearson score)
    num = pSum - (sum1*sum2/len(v1))
    den = sqrt((sum1Sq-pow(sum1,2)/len(v1)) * (sum2Sq-pow(sum2,2)/len(v1)))
    if den == 0: return 0

    return 1.0 - num/ den


class bicluster(object):
    def __init__(self, vec, left=None, right=None, distance = 0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def hcluster(data,distance=pearson):
    distances = {}
    currentClustId = -1

    #Clusters are initially just the users
    clust = [bicluster(data[i].items(),id=i) for i in range(len(data))]

    while len(clust) > 1:
        lowestpair = (0,1)
        closest = distance(clust[0].vec,clust[1].vec)
        #loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                #distances is the cache of distance calculations
                if (clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id)] = distance(clust[i].vec,clust[j].vec)

                d = distances[(clust[i].id,clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i,j)

        #calculate the average of the two clusters
        mergevec = [(clust[0].vec[i][0], (clust[lowestpair[0]].vec[i][1] + clust[lowestpair[1]].vec[i][1])/2.0) for i in range(len(clust[0].vec))]

        #Create the new cluster
        newcluster = bicluster(mergevec,left=clust[lowestpair[0]],right=clust[lowestpair[1]], distance=closest, id=currentClustId)

        #clusters ids that weren't in the original set are negative
        currentClustId-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def printclust(clust,labels=None,n=0):
    # indent to make a hierarchy layout
    for i in range(n): print ' ',
    if clust.id<0:
        # negative id means that this is branch
        print '-'
    else:
        # positive id means that this is an endpoint
        if labels==None:
            print clust.id
        else:
            print labels[clust.id]

    # now print the right and left branches
    if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
    if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)


wordCounts = {'1':{'copa': 2, 'futebol': 2, 'copa': 2, 'brasil': 1},
        '2':{'tenis': 2, 'futebol': 3, 'copa': 2, 'voley': 1},
        '3': {'basquete': 3, 'futebol': 3, 'copa': 2, 'voley': 1}}

apCount = {'copa': 3, 'brasil': 2, 'futebol': 3, 'voley': 4,
            'tenis': 5, 'basquete': 4}

#Select all the useful data
wordlist = []
for word, bc in apCount.items():
    wordlist.append(word)


#Join all together for parse it into the cluster algorithm
socialNetworking = {}

for user,wc in wordCounts.items():
    socialNetworking[user] = {}
    for word in wordlist:
        socialNetworking[user].setdefault(word,0)
        if word in wc:
            socialNetworking[user][word] = wc[word]

items = socialNetworking.items()
users = [item[0] for item in items]
data = [item[1] for item in items]

print users, data

result,clusters = kmeans.kcluster(g,users,data,k=15)

#Step 3: Showing the results
#clust = hcluster(data)
#drawDendogram(clust,labels=users)

#error,coords = scaledown(data,pearson)
#draw2d(coords,users,jpeg='twitters2D.jpg')
