<template lang="pug">
.navbar
  .logo
    router-link(to='home')
      img(src='../assets/images/dna_weaver_logo.svg')
  //- el-menu(mode='horizontal')
  //-   el-menu-item(index='home') Home
  //-   el-menu-item(index='help') Help
  //-   el-menu-item(index='about') About
</template>

<style lang='scss' scoped>

.navbar {
  display: block;
  width: auto;
  margin-bottom: 40px;
  text-align: center;
}

.el-menu {
  display: inline-block;
  border-bottom: 0px solid #dddddd;
  margin: 0 auto;
  text-align: center;
}

.el-menu-item {

}

.logo {
  display: block;
  height:80px;
  img {
    height:100%;
  }
}

</style>
