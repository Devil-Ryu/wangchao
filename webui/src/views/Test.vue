<template>
    <div>
      <input type="file" @change="handleFileChange" accept="image/*" />
      <canvas ref="canvas" :width="canvasWidth" :height="canvasHeight" @mousedown="handleMouseDown" @mousemove="handleMouseMove" @mouseup="handleMouseUp"></canvas>
      <button @click="finishDrawing">Finish Drawing</button>
      <div v-if="drawingFinished">Rectangle: {{ rectInfo }}</div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue';
  
  export default {
    setup() {
      const canvas = ref(null);
      const canvasWidth = 400; // canvas宽度
      const canvasHeight = 300; // canvas高度
      let image = new Image();
      let imageUrl = '';
      let rectStartX = 0;
      let rectStartY = 0;
      let rectEndX = 0;
      let rectEndY = 0;
      let isDrawing = false;
      let drawingFinished = false;
  
      const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            imageUrl = e.target.result; // 将图片转换成Base64格式
            image.src = imageUrl;
            image.onload = drawImageOnCanvas;
          };
          reader.readAsDataURL(file);
        }
      };
  
      const drawImageOnCanvas = () => {
        const ctx = canvas.value.getContext('2d');
        ctx.drawImage(image, 0, 0, canvasWidth, canvasHeight);
      };
  
      const handleMouseDown = (e) => {
        isDrawing = true;
        rectStartX = e.offsetX;
        rectStartY = e.offsetY;
        rectEndX = e.offsetX;
        rectEndY = e.offsetY;
      };
  
      const handleMouseMove = (e) => {
        if (isDrawing) {
          rectEndX = e.offsetX;
          rectEndY = e.offsetY;
          drawCanvas();
          drawRectangle(rectStartX, rectStartY, rectEndX, rectEndY);
        }
      };
  
      const handleMouseUp = () => {
        isDrawing = false;
      };
  
      const drawCanvas = () => {
        const ctx = canvas.value.getContext('2d');
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        ctx.drawImage(image, 0, 0, canvasWidth, canvasHeight);
      };
  
      const drawRectangle = (x1, y1, x2, y2) => {
        const ctx = canvas.value.getContext('2d');
        ctx.strokeStyle = 'red';
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
      };
  
      const finishDrawing = () => {
        drawingFinished = true;
      };
  
      // 计算矩形框信息
      const rectInfo = computed(() => {
        const width = Math.abs(rectEndX - rectStartX);
        const height = Math.abs(rectEndY - rectStartY);
        return `X: ${rectStartX}, Y: ${rectStartY}, Width: ${width}, Height: ${height}`;
      });
  
      return {
        canvas,
        canvasWidth,
        canvasHeight,
        handleFileChange,
        handleMouseDown,
        handleMouseMove,
        handleMouseUp,
        finishDrawing,
        rectInfo,
        drawingFinished,
      };
    },
  };
  </script>
  