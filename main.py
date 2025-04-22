import folium
from folium.plugins import AntPath
from geopy.distance import geodesic

# 날짜별 장소와 내용 정의
locations_by_day = {
    "4/25": [
        {"name": "하노이공항", "coords": [21.2413, 105.8011], "time": "0:00", "activity": "공항 도착"},
        {"name": "소조 호텔", "coords": [21.0049, 105.8232], "time": "1:00", "activity": "호텔 이동"},
        {"name": "노보텔 타이 하", "coords": [21.0077, 105.8239], "time": "10:00", "activity": "호텔 이동"},
        {"name": "성요셉 성당", "coords": [21.0285, 105.8491], "time": "10:30", "activity": "사진 촬영 이동"},
        {"name": "호안끼엠 호수", "coords": [21.0285, 105.8520], "time": "11:00", "activity": "사진촬영"},
        {"name": "분보남보", "coords": [21.0316, 105.8506], "time": "12:00", "activity": "점심"},
        {"name": "콩카페", "coords": [21.0332, 105.8493], "time": "13:00", "activity": "티타임"},
        {"name": "탕롱수상인형극장", "coords": [21.0335, 105.8530], "time": "18:30", "activity": "수상극"},
    ],
    "4/26": [
        {"name": "메가그랜드월드", "coords": [21.0010, 105.8501], "time": "11:00", "activity": "관광"},
        {"name": "강푸스 식당", "coords": [21.0025, 105.8525], "time": "13:00", "activity": "한식"},
        {"name": "피자포피스", "coords": [21.0338, 105.8500], "time": "18:30", "activity": "저녁 및 간단주류"},
        {"name": "롯데 스카이타워", "coords": [21.0203, 105.8593], "time": "20:00", "activity": "전망대"},
    ],
    "4/27": [
        {"name": "다이아몬드 킹", "coords": [21.0064, 105.8504], "time": "10:00", "activity": "호텔 이동"},
        {"name": "못꼿 사원", "coords": [21.0255, 105.8333], "time": "11:00", "activity": "관광"},
        {"name": "스타벅스", "coords": [21.0332, 105.8493], "time": "13:30", "activity": "카페"},
        {"name": "로즈 키친", "coords": [21.0272, 105.8546], "time": "15:00", "activity": "쿠킹클래스"},
        {"name": "기찻길", "coords": [21.0335, 105.8562], "time": "18:00", "activity": "기찻길 사진찍기"},
        {"name": "하노이공항", "coords": [21.2413, 105.8011], "time": "0:00", "activity": "공항 도착"},

    ],
    # 날짜별로 장소 추가 가능
}

# 이동 속도 설정 (km/h)
walk_speed_kmh = 5.0
taxi_speed_kmh = 20.3

# 전체 경로 지도 (day_total)
m_total = folium.Map(location=[21.0285, 105.85], zoom_start=14, tiles='CartoDB Positron')

# 날짜별 색상 설정 (각 날짜마다 다른 색상)
colors = {
    "4/25": 'red',
    "4/26": 'blue',
    "4/27": 'green',
}

# 날짜별 지도 만들기
for day_idx, (day, locations) in enumerate(locations_by_day.items(), start=1):
    m = folium.Map(location=[21.0285, 105.85], zoom_start=14, tiles='CartoDB Positron')
    
    # 마커 추가
    for i, loc in enumerate(locations):
        # 장소 이름을 지도에 직접 표시
        folium.Marker(
            location=loc["coords"],
            popup=f"{loc['name']} - {loc['time']} - {loc['activity']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

        # 각 날짜에 번호 추가 (순서대로)
        folium.Marker(
            location=loc["coords"],
            popup=f"{i+1}",
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)

    # 경로 및 이동 시간 정보 표시
    coords = [loc["coords"] for loc in locations]
    for i in range(len(coords) - 1):
        start = coords[i]
        end = coords[i + 1]
        distance_km = geodesic(start, end).km

        # 시간 계산 (분 단위)
        walk_time_min = (distance_km / walk_speed_kmh) * 60
        taxi_time_min = (distance_km / taxi_speed_kmh) * 60

        # 경로 그리기
        AntPath([start, end], color=colors[day], weight=4, dash_array=[10, 20]).add_to(m)

        # 중간 지점에 이동 시간 마커 표시
        mid_lat = (start[0] + end[0]) / 2
        mid_lon = (start[1] + end[1]) / 2
        folium.Marker(
            location=[mid_lat, mid_lon],
            icon=folium.DivIcon(html=f'''
                <div style="
                    font-size:10pt; 
                    color:green; 
                    background-color: white; 
                    padding: 2px 6px; 
                    border-radius: 6px; 
                    box-shadow: 1px 1px 3px rgba(0,0,0,0.3); 
                    white-space: nowrap;">
                    🚶 {int(walk_time_min)}분 &nbsp;&nbsp; 🚖 {int(taxi_time_min)}분
                </div>
            ''')
        ).add_to(m)

    # 날짜별 파일 저장
    map_filename = f'map/day_{day_idx}.html'
    m.save(map_filename)
    print(f'{map_filename} has been saved.')

    # day_total 지도에 각 날짜의 경로 추가
    coords = [loc["coords"] for loc in locations]
    for i in range(len(coords) - 1):
        start = coords[i]
        end = coords[i + 1]
        AntPath([start, end], color=colors[day], weight=4, dash_array=[10, 20]).add_to(m_total)

# 전체 경로 지도 저장
m_total.save('map/day_total.html')
print('map/day_total.html has been saved.')