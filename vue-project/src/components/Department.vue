<template>
  <div class="department">
    <h2>系所介紹</h2>
    <p class="subtitle">探索各系所特色，找到你的志向</p>
    <div class="departments-list">
      <div class="dept-card" v-for="dept in departments" :key="dept.name">
        <div class="dept-title">{{ dept.name }}</div>
        <div class="dept-desc">{{ dept.desc }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const departments = [
  { name: '英語教學中心', desc: '強化英語教學與國際溝通能力' },
  { name: '體育室', desc: '推動體育活動與健康促進' },
  { name: '數位媒體設計學系', desc: '數位影像、互動設計與多媒體創作' },
  { name: '企業管理學系', desc: '管理理論、創業與企業經營' },
  { name: '資訊管理學系', desc: '資訊系統、資料分析與管理實務' },
  { name: '觀光事業學系', desc: '旅遊管理、飯店經營與休閒規劃' },
  { name: '影音新聞暨社群傳播學系', desc: '影音新聞、社群媒體與傳播素養' },
  { name: '應用統計與資料科學學系', desc: '統計分析、資料科學與大數據應用' },
  { name: '休閒遊憩管理學系', desc: '休閒活動規劃與管理' },
  { name: '餐旅管理學系', desc: '餐飲、旅館與服務管理' },
  { name: '商業設計學系', desc: '結合設計美學與商業行銷' },
  { name: '商品設計學系', desc: '產品設計、創新與市場導向' },
  { name: '建築學系', desc: '建築設計、都市規劃與空間美學' },
  { name: '廣告暨策略行銷學系', desc: '廣告創意、行銷與策略規劃' },
  { name: '新聞與大眾傳播學士學位學程', desc: '新聞採訪、編輯與媒體素養' },
  { name: '傳播學院', desc: '整合新聞、廣告、媒體等傳播領域' },
  { name: '新媒體暨傳播管理學系', desc: '新媒體技術與傳播管理' },
  { name: '廣播電視學系', desc: '廣播、電視與媒體製作' },
  { name: '資訊工程學系', desc: '程式設計、AI、雲端技術與軟體開發' },
  { name: '犯罪防治學系', desc: '犯罪學、司法與防治實務' },
  { name: '生物科技學系', desc: '生物技術、醫學與產業應用' },
  { name: '醫療資訊與管理學系', desc: '結合醫療與資訊科技，推動智慧健康' },
  { name: '法律學系', desc: '法學理論與實務，培養法律專業人才' },
  { name: '應用英語學系', desc: '強化英語聽說讀寫，培養國際溝通能力' },
  { name: '應用日語學系', desc: '日語語言、文化與溝通能力' },
  { name: '金融科技應用學士學位學程', desc: '金融科技、創新應用與管理' },
  { name: '旅遊與觀光學士學位學程', desc: '旅遊規劃與觀光管理' },
  { name: '會計學系', desc: '會計理論、審計與財務報表分析' },
  { name: '資訊應用與金融保險學系', desc: '資訊應用、金融與保險管理' },
  { name: '財務金融學系', desc: '金融理論、投資管理與財務分析' },
  { name: '國際企業學系', desc: '國際企業管理與全球市場' },
  { name: '國際事務與外交學士學位學程', desc: '國際關係、外交政策與全球議題' },
  { name: '諮商臨床與工商心理學系', desc: '心理學理論、諮商與臨床應用' },
  { name: '諮商臨床與工商心理學系碩士班諮商心理學組', desc: '諮商心理學專業培訓' },
  { name: '諮商臨床與工商心理學系碩士班臨床心理學組', desc: '臨床心理學專業培訓' },
  { name: '金融學系', desc: '金融理論、金融市場與管理' },
  { name: '財金法律學系', desc: '財金、法律與金融法規' },
  { name: '生物醫學工程學系', desc: '生物醫學、工程與健康應用' },
  { name: '公共事務與行政管理學系', desc: '公共事務、政策與行政管理' },
  { name: '高階經理碩士在職學位學程', desc: '高階管理與領導力培訓' },
  { name: '都市設計與永續發展學系', desc: '都市設計、永續發展與規劃' },
  { name: '人工智慧應用學系', desc: '人工智慧技術與應用' },
  { name: '半導體應用學士學位學程', desc: '半導體技術與產業應用' },
  { name: '應用中文與華語文教學系', desc: '中文語言、華語教學與文化' },
  { name: '教育研究所', desc: '教育理論與研究' },
  { name: '電機工程學系', desc: '電力、控制、通訊與能源領域專業' },
  { name: '金融科技應用學系', desc: '金融科技、創新應用與管理' },
  { name: '時尚與創新管理學士學位學程', desc: '時尚產業與創新管理' },
  { name: '資訊科技應用與管理學士學位學程', desc: '資訊科技應用與管理' },
  { name: '國際事務碩士學位學程', desc: '國際事務與外交專業培訓' },
  { name: '國際企業與貿易學士學位學程', desc: '國際企業與貿易管理' },
  { name: '金融科技碩士學位學程', desc: '金融科技專業培訓' },
  { name: '國防行政管理進修學士學位學程', desc: '國防行政與管理' },
  { name: '國際班', desc: '國際化課程與多元文化交流' },
  { name: '金門校區(不分系所)', desc: '金門校區綜合課程' }
]
</script>
<script>
export default {
  name: 'Department'
}
</script>

<style scoped>
.department {
  display: flex;
  flex-direction: column;
}
h2 {
  color: #8e44ad;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 8px;
}
.subtitle {
  color: #38c9fa;
  font-size: 1.1rem;
  margin-bottom: 18px;
  font-weight: 500;
}
.departments-list {
  display: flex;
  gap: 18px;
  margin-top: 10px;
  flex-wrap: wrap;
  justify-content: center;
}
.dept-card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(80,120,255,0.10);
  padding: 18px 22px;
  min-width: 160px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.dept-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: #8e44ad;
  margin-bottom: 6px;
}
.dept-desc {
  font-size: 0.95rem;
  color: #888;
}
</style>
