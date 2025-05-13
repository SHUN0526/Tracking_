import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1) 파일 경로 (환경에 맞춰 수정하세요)
file_path = "C:\\Users\\soong\\OneDrive\\바탕 화면\\Exp\\test_YTH_M25_P1 - 복사본.csv"
# 2) CSV 읽기 및 컬럼명 정리
df = pd.read_csv(file_path)
df = df.rename(columns={
    'timestamp(ms)': 'timestamp_ms',
    'eda(uS)':      'eda',
    'bpm':          'bpm',
    'ibi(ms)':      'ibi'
})

# 3) 60번째 행부터 슬라이스
df_slice = df.iloc[5:-5].reset_index(drop=True)

# 4) 시간 벡터 (시작점을 0으로 맞춤)
t0     = df_slice['timestamp_ms'].iloc[0]
time_s = (df_slice['timestamp_ms'] - t0) / 1000.0

# 5) HRV 지표 계산
# 정상 범위 예시: 300ms < IBI < 1500ms
ibi = df_slice['ibi']
ibi_clean = ibi[(ibi >   300) & (ibi < 1500)]
rr    = ibi_clean
mean_rr = rr.mean()
sdnn    = rr.std(ddof=1)
rmssd   = np.sqrt(np.mean(rr.diff().dropna()**2))
print(f"Mean RR: {mean_rr:.2f} ms   SDNN: {sdnn:.2f} ms   RMSSD: {rmssd:.2f} ms")

# 5-1) eda 및 bpm의 평균 및 표준편차 계산
eda_mean = df_slice['eda'].mean()
eda_std  = df_slice['eda'].std(ddof=1)
bpm_mean = df_slice['bpm'].mean()
bpm_std  = df_slice['bpm'].std(ddof=1)
print(f"EDA Mean: {eda_mean:.2f} µS   EDA Std: {eda_std:.2f} µS")
print(f"BPM Mean: {bpm_mean:.2f} bpm   BPM Std: {bpm_std:.2f} bpm")


# 6) 한 창에 두 개의 서브플롯 생성
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# EDA 플롯
ax1.plot(time_s, df_slice['eda'], label='EDA')
ax1.set_ylabel('EDA (µS)')
ax1.set_title('EDA over Time (from 60th row)')
ax1.grid(True)
ax1.legend()

# BPM 플롯
ax2.plot(time_s, df_slice['bpm'], label='BPM', color='tab:orange')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('BPM')
ax2.set_title('BPM over Time (from 60th row)')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()