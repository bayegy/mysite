from nature import Nature
import time
print("sleeping....")
time.sleep(3600 * 12)

np = Nature('NATURE')
nature_journals = [i for i in np.journals_info.keys() if not(i.find('NATURE') == -1 and i.find('Nature') == -1)]

for jn in nature_journals:
    print(jn)
    try:
        n = Nature(jn)
        n.update_db_papers()
        n.net.close()
    except Exception as e:
        print(e)
        print(n.url)
