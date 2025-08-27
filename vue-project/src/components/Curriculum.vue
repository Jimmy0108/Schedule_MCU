
<template>
  <div class="curriculum">
    <h2>課程架構</h2>
    <p class="subtitle">一目了然的課程規劃，輕鬆掌握學習進度</p>
    <div class="curriculum-table">
      <div class="table-row table-header">
        <div>年級</div>
        <div>必修</div>
        <div>選修</div>
      </div>
      <div class="table-row" v-for="row in rows" :key="row.grade">
        <div>{{ row.grade }}</div>
        <div>{{ row.required }}</div>
        <div>{{ row.elective }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const rows = [
  { grade: '一年級', required: '程式設計、微積分', elective: '英文、體育' },
  { grade: '二年級', required: '電子學、線性代數', elective: '創新思維' },
  { grade: '三年級', required: '資料結構、機率統計', elective: '專題研究' },
  { grade: '四年級', required: '專業實習', elective: '職涯規劃' }
]
</script>
<script>
export default {
  name: 'Curriculum'
}
</script>

<style scoped>
.curriculum {
  display: flex;
  flex-direction: column;
}
h2 {
  color: #16a085;
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
.curriculum-table {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(80,120,255,0.10);
  padding: 18px 22px;
  min-width: 260px;
  margin-top: 10px;
}
.table-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}
.table-header {
  font-weight: 600;
  color: #4f8cff;
  border-bottom: 2px solid #38c9fa;
}
.table-row:last-child {
  border-bottom: none;
}
</style>
