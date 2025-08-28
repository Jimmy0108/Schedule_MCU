
<template>
  <div class="main-screen">
    <h2 class="fade-in-down">銘傳大學 電機工程學系</h2>
    <p class="subtitle fade-in-down" style="animation-delay: 0.2s;">理論與實務並重，接軌未來科技</p>
    <button @click="goToCourseSelection" class="cta-button fade-in-up">開始選課</button>

    <div class="features fade-in-up" style="animation-delay: 0.4s;">
      <div class="feature-card">
        <span class="icon">📚</span>
        <h3>課程與教學</h3>
        <p>課程涵蓋電路學、電子學、電磁學等基礎，結合資訊技術，強調「做中學」，實務與理論並重。</p>
      </div>
      <div class="feature-card">
        <span class="icon">🔬</span>
        <h3>研究與資源</h3>
        <p>設有機器人、智慧網路、通訊、晶片設計等實驗室，提供豐富的學習與研究資源。</p>
      </div>
      <div class="feature-card">
        <span class="icon">🎓</span>
        <h3>畢業與發展</h3>
        <p>畢業生出路寬廣，所學不僅涵蓋硬體，也重視軟體與系統整合能力，能投入各種高科技產業。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['navigate']);

function goToCourseSelection() {
  emit('navigate', 'course');
}
</script>

<style scoped>
.main-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
}
h2 {
  color: #4f8cff;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 8px;
}
.subtitle {
  color: #38c9fa;
  font-size: 1.2rem;
  margin-bottom: 24px;
  font-weight: 500;
}
.cta-button {
  background: linear-gradient(90deg, #4f8cff 0%, #38c9fa 100%);
  color: white;
  border: none;
  padding: 14px 32px;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 50px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.features {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 4rem;
  max-width: 1000px;
}
.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  flex: 1;
  min-width: 220px;
}
.feature-card .icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  display: inline-block;
}
.feature-card h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #4f8cff;
}
.feature-card p {
  color: #666;
  line-height: 1.6;
}

/* Animations */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.fade-in-down {
  animation: fadeInDown 0.5s ease-out forwards;
}
.fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
}
</style>
