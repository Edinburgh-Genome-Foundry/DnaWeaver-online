<template lang='pug'>
#website
  .page
    navbar
  router-view
  footersection
  </div>
</template>

<script>
import navbar from './components/Navbar.vue'
import footersection from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    navbar,
    footersection
  }
}
</script>

<style>
@import './assets/css/animate.css';
@import url(https://fonts.googleapis.com/css?family=Open+Sans);
@import url(https://fonts.googleapis.com/css?family=Inconsolata);
@import url(https://fonts.googleapis.com/css?family=Raleway);

body {
  font-family: 'Open Sans', 'Source Sans Pro',  Helvetica, Arial, sans-serif;
}

#website {
  font-family: 'Open Sans', 'Source Sans Pro',  Helvetica, Arial, sans-serif;
  font-size:16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
