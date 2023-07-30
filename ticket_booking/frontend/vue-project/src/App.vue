<template>
  <div id="app">
    <NavBar />
    <router-view></router-view>
  </div>
</template>

<script setup>
import NavBar from "./components/NavBar.vue"

// export default {
//   name: 'App',
// };
</script>

<style>
/* Import the common CSS file */
@import "@/assets/styles.css";
</style>


