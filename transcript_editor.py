import pysrt
import pandas as pd

def transcript_to_pitch():
    data = pd.read_csv("Data/SharkTankUSdataset.csv")
    data = data[['Season Number', 'Episode Number', 'Pitch Number', 'Entrepreneur Names']]
    seasons = data['Season Number'].tolist()
    for s in seasons:
        episodes = data[(data['Season Number'] == s)]
        episodes = episodes['Episode Number'].tolist()
        for ep in episodes:
            subs = pysrt.open("data/Transcripts/1/Shark Tank - S{s}E{ep} [English Sub].srt")
            ep_data = data[(data['Season Number'] == s) & (data['Episode Number'] == ep)]
            entr_names = ep_data['Entrepreneur Names'].str.split(',').tolist()
            prev_pitch_num = min(ep_data['Pitch Number'].tolist()) - 1
            segments = [[]]
            seg_abt = [[]]
            for i in range(len(subs)):
                if subs[i].text == '♪♪♪':
                    segments.append([])
                    seg_abt.append([])
                else:
                    segments[-1].append(subs[i].text.split('\n'))
                    for pitch_num, pitch_names in enumerate(entr_names):
                        for name in pitch_names:
                            if str.upper(name) in subs[i].text and 'NEXT' not in subs[i].text:
                                seg_abt[-1].append(prev_pitch_num + pitch_num)
            # for i in len(segments):
                # if 

def main():
    transcript_to_pitch()
    

if __name__ == "__main__":
    main()