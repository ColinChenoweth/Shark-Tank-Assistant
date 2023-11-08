import pysrt
import pandas as pd
import os

def transcript_to_pitch():
    data = pd.read_csv("Data/SharkTankUSdataset.csv")
    data = data[['Season Number', 'Episode Number', 'Pitch Number', 'Entrepreneur Names']]
    seasons = data['Season Number'].unique().tolist()
    for s in seasons:
        episodes = data[(data['Season Number'] == s)]
        episodes = episodes['Episode Number'].unique().tolist()
        for ep in episodes:
            try:
                subs = pysrt.open("data/Transcripts/%s/Shark Tank - S%sE%s [English Sub].srt" % (s, s, ep))
            except:
                continue
            ep_data = data[(data['Season Number'] == s) & (data['Episode Number'] == ep)]
            entr_names = ep_data['Entrepreneur Names'].str.split(r'[, ]' or 'and').tolist()
            prev_pitch_num = min(ep_data['Pitch Number'].tolist())
            segments = [[]]
            seg_abt = [[]]
            for i in range(len(subs)):
                if subs[i].text == '♪♪♪' or subs[i].text == '♪♪':
                    segments.append([])
                    seg_abt.append([])
                else:
                    try:
                        for pitch_num, pitch_names in enumerate(entr_names):
                            for name in pitch_names:
                                if "<i>" == subs[i].text[0:3] and "</i>" == subs[i].text[-4:]:
                                    break
                                if name != ''  and name != 'and' and str.upper(name) in str.upper(subs[i].text) and 'NEXT' not in str.upper(subs[i].text):
                                    # seg_abt[-1].append(prev_pitch_num + pitch_num)
                                    seg_abt.append([prev_pitch_num + pitch_num])
                                    segments.append([])
                                    break
                        if "<i>" != subs[i].text[0:3] and "</i>" != subs[i].text[-4:]:      
                            segments[-1].append(subs[i].text.split('\n'))
                    except:
                        print("ERROR for Season %s Episode %s" % (s, ep))


            for i in range(len(segments)):
                if not seg_abt[i]:
                    next
                else:
                    p = seg_abt[i][0]
                    if all(p == p_opt for p_opt in seg_abt[i]):
                        directory_name = "Data/Pitch_Transcripts/Season_%s/Episode_%s" % (s, ep)
                        file_name = "Pitch_%s.txt" % p
                        if not os.path.exists(directory_name):
                            os.makedirs(directory_name)
                        file_path = os.path.join(directory_name, file_name)
                        with open(file_path, 'a', errors='replace') as file:
                            for seg_item in segments[i]:
                                for line in seg_item:
                                    file.write("%s\n" % line)
                    else:
                        print("ERROR: Season %s, Episode %s, Pitch %s" % (s, ep, p))
                        return

                

def main():
    transcript_to_pitch()
    

if __name__ == "__main__":
    main()