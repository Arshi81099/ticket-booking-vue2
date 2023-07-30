<template>
    <div id="slider" class="slider">
      <ul class="slides" :style="{ left: -width * current + 'px' }">
        <li v-for="(slide, i) in slides" :key="i">
          <img :src="slide.img" alt="slide.alt">
        </li>
      </ul>
      <ul class="bullets">
        <li v-for="(slide, i) in slides" @click="selectSlide(i)" :key="i" v-html="i === current ? '&#9679;' : '&omicron;'"></li>
      </ul>
      <a class="prev" href="#" @click.prevent="prevSlide">&#x25C0;</a>
      <a class="next" href="#" @click.prevent="nextSlide">&#x25B6;</a>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        slides: [


          {
            image: require('../assets/movie4.jpeg'),
            alt: 'Slide 1',
          },
          {
            image: require('../assets/movie3.png'),
            alt: 'Slide 2',
          },
          {
            image: require('../assets/movie2.jpeg'),
            alt: 'Slide 3',
          },
          {
            image: require('../assets/movie1.jpeg'),
            alt: 'Slide 4',
          },
        ],
        current: 0,
        width: 800,
        timer: 0,
      };
    },
    methods: {
      nextSlide() {
        this.current++;
        if (this.current >= this.slides.length) this.current = 0;
        this.resetPlay();
      },
      prevSlide() {
        this.current--;
        if (this.current < 0) this.current = this.slides.length - 1;
        this.resetPlay();
      },
      selectSlide(i) {
        this.current = i;
        this.resetPlay();
      },
      resetPlay() {
        clearInterval(this.timer);
        this.play();
      },
      play() {
        let app = this;
        this.timer = setInterval(function () {
          app.nextSlide();
        }, 2000);
      },
    },
    created() {
      this.play();
    },
  };
  </script>
  
  <style>
  #slider {
    width: 100%;
  }
  
  .slider {
    margin: 0 auto;
    padding: 0;
    width: 800px;
    height: 400px;
    position: relative;
    overflow: hidden;
  }
  
  ul.slides {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    display: table;
    position: absolute;
    top: 0;
    transition: left 800ms;
  }
  
  ul.slides li {
    list-style-type: none;
    display: table-cell;
  }
  
  ul.slides li img {
    width: 800px;
  }
  
  ul.bullets {
    width: inherit;
    position: absolute;
    bottom: 0;
    left: 0;
    padding: 0;
    margin: 0 0 10px 0;
    text-align: center;
    z-index: 1;
  }
  
  ul.bullets li {
    list-style-type: none;
    display: inline;
    color: #fff;
    cursor: pointer;
    padding: 0 5px;
    font-size: 20px;
    font-family: sans-serif;
  }
  
  .prev,
  .next {
    text-decoration: none;
    color: #fff;
    position: absolute;
    z-index: 1;
    font-size: 42px;
    top: 43%;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
  }
  
  .prev {
    left: 20px;
  }
  
  .next {
    right: 20px;
  }
  </style>
  