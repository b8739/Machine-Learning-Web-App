# Machine Learning Web App 

머신러닝의 기본 프로세스, 데이터 전처리부터, EDA (Explorative Data Analysis), 모델링까지 GUI로 쉽고 간편하게 이용할 수 있는 웹 서비스입니다.

엑셀의 시트 같은 기능으로 데이터를 버전별로 관리하고, Data Aggregation Pipeline을 통해 데이터 분석에 필수적인 데이터 전처리를 수행할 수 있습니다.

## **📚기술 스택**

<div align="center">
     <img src="https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white"> 
          <img src="https://img.shields.io/badge/vuex-1c2e4a?style=for-the-badge&logo=vue.js&logoColor=white"> 
    <img src="https://img.shields.io/badge/vuetify-%231867C0.svg?&style=for-the-badge&logo=vuetify&logoColor=white"/>
    	
</div>
<div align="center">
<img src="https://img.shields.io/badge/html5-%23E34F26.svg?&style=for-the-badge&logo=html5&logoColor=white" />
	<img src="https://img.shields.io/badge/css3-%231572B6.svg?&style=for-the-badge&logo=css3&logoColor=white" />
<img src="https://img.shields.io/badge/javascript-%23F7DF1E.svg?&style=for-the-badge&logo=javascript&logoColor=black" />

</div>

<div align="center">
	<img src="https://img.shields.io/badge/flask-%23000000.svg?&style=for-the-badge&logo=flask&logoColor=white" />
    <img src="https://img.shields.io/badge/python-%233776AB.svg?&style=for-the-badge&logo=python&logoColor=white" />
</div>

<div align="center">
	<img src="https://img.shields.io/badge/mongodb-%2347A248.svg?&style=for-the-badge&logo=mongodb&logoColor=white" />
    <img src="https://img.shields.io/badge/ELASTIC BEANSTALK-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white">
</div>
<div align="center">
	 <img src="https://img.shields.io/badge/plotly-%233F4F75.svg?&style=for-the-badge&logo=plotly&logoColor=white" />
    <img src="https://img.shields.io/badge/webgl-990000?style=for-the-badge&logo=webgl&logoColor=white">
    <img src="https://img.shields.io/badge/fontawesome-339AF0?style=for-the-badge&logo=fontawesome&logoColor=white">
</div>

<div align="center">

</div>

---

## 🧐 본 웹 어플리케이션의 핵심 기능

어플리케이션의 기능은 크게 Preprocess, EDA, Modeling으로 나뉘어집니다.

## **Preprocess**

![](https://velog.velcdn.com/images/a87380/post/912008a8-a81e-47f5-aa8e-9fd09b96fc83/image.gif)

🔎 **기본 기능**

- 데이터 (csv/xlsx 파일)를 테이블 형태로 화면 상에 불러오고, 기본적인 데이터 전처리 (Row 삭제, Column 삭제, Tag 이름 변경, NA 처리) 등의 기능들을 수행할 수 있습니다.
- 데이터의 Summary Statistics (mean, median, mode 등) 테이블을 제공합니다.
- 전처리한 데이터를 Excel 파일로 Export할 수 있습니다.
- 전처리한 데이터를 데이터베이스에 저장하고, 이후 똑같이 불러와서 이어서 진행할 수 있습니다.

✅ **차별점**

- **Draft Version 관리:**
  ![](https://velog.velcdn.com/images/a87380/post/bd8a897b-7706-4dad-9aa1-6ad361deef31/image.gif)

  - 엑셀의 시트처럼 동일한 데이터에 한해서 여러 Draft Version만들고, 저장하고, 활용할 수 있습니다. (각 버전마다 전처리를 다르게 해서 다른 모델링 결과를 보려고 할 때 유용합니다)
  - 전처리 할 때 MongoDB의 Aggregation을 활용하기 때문에, **원본을 유지한 체** 여러 버전을 만들 수 있습니다.

- **Data Aggregation**:
  ![](https://velog.velcdn.com/images/a87380/post/a72d63d6-a758-4c45-a6de-1bd6cb953a50/image.gif)
  - MongoDB의 Aggregation을 활용하여, 각 Tag에 대하여 조건 (Equals, Greater than, Less than)을 부여해서 데이터를 필터링 할 수 있습니다.
- **Lazy Loading:**
  ![](https://velog.velcdn.com/images/a87380/post/3fbb46e6-e216-4b08-a8cb-a67751837d44/image.gif)
  - Lazy Loading 라이브러리 중 하나인 Infinite Loading을 활용하여, 용량이 큰 데이터를 테이블로 불러사용자의 UX를 헤치지 않습니다.

---

## **EDA**

![](https://velog.velcdn.com/images/a87380/post/ac3c49b3-9da6-422d-8fa2-33fe9e0ac0b3/image.gif)
🔎 **기본 기능**

- Plotly 라이브러리를 활용하여 데이터를 웹 상에 시각화합니다.

✅ **차별점**

- **Preprocess와의 호환:**
  - 단순히 원본 데이터의 그래프로 불러오는 것이 아니라, 데이터를 전처리할 때마다 업데이트된 상태의 데이터를 업데이트할 수 있습니다.
- **화면 분할:**
  - EDA 페이지가 화면의 전체를 차지하는 것이 아니라, 전처리 화면 옆에 서랍처럼 꺼내어서 그래프를 불러올 수 있기 때문에, 전처리의 흐름을 깨뜨리지 않습니다.

---

## **Modeling**

🔎 **기본 기능:**

- XGBoost, SVR, Random Forest 알고리즘을 활용한 모델링을 수행하고, 결과를 확인 및 저장할 수 있습니다.

✅ **차별점**
![](https://velog.velcdn.com/images/a87380/post/ff37d2b6-45e5-414f-a89c-688dde4d4e18/image.gif)

- **Canvas를 통한 Modeling 설계**
  - GUI처럼 Canvas 화면에서 Input 태그, Output 태그, 알고리즘 등을 Node 형태로 추가하고, 이 Node들을 마우스로 연결해서 사용하기 때문에, 보다 직관적으로 모델링을 설계할 수 있습니다.
- **Modeling 결과**
  - Plotly 라이브러리를 활용하여, Actual과 Predictive 값을 예측한 비교 그래프, 그리고 Prediction Power (R^2, MAPE, RMSE 값)등을 시각적으로 확인할 수 있습니다.


