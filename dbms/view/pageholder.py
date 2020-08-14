from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

Capacity=5
pages=7
leftneibor=2
rightneibor=3

def pageBuilder(data,page):
    page=int(page)
    right=rightneibor
    left=leftneibor
    neibor=left+right
    pagenator=Paginator(data,Capacity)

    #从前端读取page
    try:
        items=pagenator.page(page)
    except PageNotAnInteger:
        items=pagenator.page(int(page))
    except EmptyPage:
        items=pagenator.page(pagenator.num_pages)

    if(items.has_next()):
        next_page_number=items.next_page_number()
    else:
        next_page_number=0
    
    if(items.has_previous()):
        previous_page_number=items.previous_page_number()
    else:
        previous_page_number=0

    print("previous_page_num:{}   next_page_num:{}".format(previous_page_number,next_page_number))
    if(next_page_number<right):
        right=next_page_number
        left=neibor-right
    if(previous_page_number<left):
        left=previous_page_number
        right=neibor-left    

    if(page-left-1>0):
        leftLowerBound=page-left-1
    else:
        leftLowerBound=1
    leftUpperBound=page-1
    rightLowerBound=page+1
    rightUpperBound=page+right
    if(rightUpperBound>20):
        rightUpperBound=20

    print("leftLowerBound:{}  leftUpperBound:{} rightLowerBound:{} rightUpperBound:{}".format(
                leftLowerBound,leftUpperBound,rightLowerBound,rightUpperBound
    ))
    rangeLeft=range(leftLowerBound,leftUpperBound+1)
    rangeRight=range(rightLowerBound,rightUpperBound+1)
    context={
        "items":items,
        "leftLowerBound":leftLowerBound,
        "leftUpperBound":leftUpperBound,
        "rightLowerBound":rightLowerBound,
        "rightUpperBound":rightUpperBound,
        "rangeLeft":rangeLeft,
        "rangeRight":rangeRight,
    }    

    return context