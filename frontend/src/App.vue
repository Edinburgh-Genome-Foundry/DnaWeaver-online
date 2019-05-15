<template lang='pug'>
#website
  github-corners(repo="Edinburgh-Genome-Foundry/dnaweaver" bg-color='#8ac1e8')
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

hr {
    border : 0;
    height: 1px;
    margin-top: 60px;
    margin-bottom: 60px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
}

a {
  color: rgb(98, 158, 237) !important;
}
</style>
