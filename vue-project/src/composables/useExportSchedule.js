import { ref, computed } from 'vue';
import html2pdf from 'html2pdf.js';
import { toPng, toJpeg, toBlob } from 'html-to-image';

export default function useExportSchedule() {
    const exportLoading = ref(false);
    const exportError = ref(null);

    // PDF 匯出選項
    const pdfOptions = {
        margin: [10, 10],
        filename: '我的課表.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' }
    };

    // 匯出為 PDF
    const exportToPDF = async (elementRef) => {
        if (!elementRef) {
            exportError.value = '找不到要匯出的元素';
            return null;
        }

        exportLoading.value = true;
        exportError.value = null;

        try {
            await html2pdf().set(pdfOptions).from(elementRef).save();
            return true;
        } catch (error) {
            console.error('PDF 匯出錯誤:', error);
            exportError.value = '匯出 PDF 時發生錯誤';
            return null;
        } finally {
            exportLoading.value = false;
        }
    };

    // 匯出為 PNG
    const exportToPNG = async (elementRef) => {
        if (!elementRef) {
            exportError.value = '找不到要匯出的元素';
            return null;
        }

        exportLoading.value = true;
        exportError.value = null;

        try {
            const dataUrl = await toPng(elementRef, { cacheBust: true, pixelRatio: 2 });

            // 創建下載連結
            const link = document.createElement('a');
            link.download = '我的課表.png';
            link.href = dataUrl;
            link.click();

            return dataUrl;
        } catch (error) {
            console.error('PNG 匯出錯誤:', error);
            exportError.value = '匯出 PNG 時發生錯誤';
            return null;
        } finally {
            exportLoading.value = false;
        }
    };

    // 匯出為 JPEG
    const exportToJPEG = async (elementRef) => {
        if (!elementRef) {
            exportError.value = '找不到要匯出的元素';
            return null;
        }

        exportLoading.value = true;
        exportError.value = null;

        try {
            const dataUrl = await toJpeg(elementRef, { cacheBust: true, quality: 0.95, pixelRatio: 2 });

            // 創建下載連結
            const link = document.createElement('a');
            link.download = '我的課表.jpg';
            link.href = dataUrl;
            link.click();

            return dataUrl;
        } catch (error) {
            console.error('JPEG 匯出錯誤:', error);
            exportError.value = '匯出 JPEG 時發生錯誤';
            return null;
        } finally {
            exportLoading.value = false;
        }
    };

    return {
        exportLoading,
        exportError,
        exportToPDF,
        exportToPNG,
        exportToJPEG
    };
}
