
<template>
  <div class="faculty">
    <h2>師資陣容</h2>
    <p class="subtitle">年輕有活力的師資團隊，陪你一起成長</p>
    <div class="faculty-list">
      <div class="faculty-card" v-for="teacher in teachers" :key="teacher.name">
        <div class="teacher-name">{{ teacher.name }}</div>
        <div class="teacher-title">{{ teacher.title }}</div>
        <div class="teacher-desc">{{ teacher.desc }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const teachers = [
  { name: '王小明', title: '副教授', desc: '專長：程式設計、AI 應用' },
  { name: '李大華', title: '教授', desc: '專長：電子學、嵌入式系統' },
  { name: '陳美麗', title: '助理教授', desc: '專長：機械設計、創新教學' }
]
</script>
<script>
export default {
  name: 'Faculty'
}
</script>

<style scoped>
.faculty {
  display: flex;
  flex-direction: column;
}
h2 {
  color: #d35400;
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
.faculty-list {
  display: flex;
  gap: 18px;
  margin-top: 10px;
  flex-wrap: wrap;
  justify-content: center;
}
.faculty-card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(80,120,255,0.10);
  padding: 18px 22px;
  min-width: 160px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.teacher-name {
  font-size: 1.15rem;
  font-weight: 600;
  color: #d35400;
  margin-bottom: 6px;
}
.teacher-title {
  font-size: 1rem;
  color: #4f8cff;
  margin-bottom: 4px;
}
.teacher-desc {
  font-size: 0.95rem;
  color: #888;
}
</style>
