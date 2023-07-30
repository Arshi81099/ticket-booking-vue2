import Vue from 'vue';
import router from './router';
import App from './App.vue';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(BootstrapVue);

import axios from 'axios';

// global Axios instance
const instance = axios.create({
  baseURL: 'http://127.0.0.1:5000/', 
});

Vue.prototype.$http = instance;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
