# Grow Castle Leveling Calculator - Icons Included

이 버전은 캐릭터 아이콘 PNG가 포함된 버전입니다.

주의:
- 포함된 이미지는 공식 게임 이미지가 아니라, 배포 가능하도록 새로 만든 오리지널 아이콘입니다.
- 공식 Grow Castle 캐릭터 일러스트를 그대로 포함하면 저작권 문제가 생길 수 있습니다.

## 실행
```bash
python main.py
```

## exe 만들기
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name GrowCastleCalculator main.py
```

또는 `build_exe.bat` 더블클릭.

## 완성 파일 위치
```text
dist/GrowCastleCalculator.exe
```

## 설정 저장
웨이브, 선택 캐릭터, 비율은 `settings.json`에 저장됩니다.
