<template lang="pug">
.file-example
  el-card
    center
      h3
        .filename {{dataFilename}}
        p.use-file(v-if='useFileButton')
          el-tooltip(content='use this file')
            el-button(@click='loadFile()') Go!
    img.small-image(v-if='imgSrc', :src='imgSrc' @click="dialogVisible = true")
    .description
      slot
  //- hr
</template>

<script>
import uuidv1 from 'uuid/v1'

export default {
  name: 'file-example',
  props: {
    fileHref: {default: () => ''},
    imgSrc: {default: () => null},
    description: {default: () => null},
    filename: {default: () => null},
    useFileButton: {default: true}
  },
  data () {
    return {
      defaultImgSrc: null,
      dataFilename: this.filename,
      dialogVisible: false
    }
  },
  methods: {
    loadFile () {
      var self = this
      this.$http.get(this.fileHref, {responseType: 'blob'}).then(function (response) {
        var reader = new window.FileReader()
        reader.onloadend = function (ev) {
          if (ev.target.readyState === window.FileReader.DONE) {
            self.$emit('input', {
              name: response.url.split('/').slice(-1)[0],
              content: ev.target.result,
              uid: uuidv1(),
              status: 'success'
            })
          }
        }
        reader.readAsDataURL(response.bodyBlob)
      })
    }
  }
}
</script>

<style lang='scss' scoped>

.file-example {
  // display: inline-block;
  // vertical-align: top;
  // width: 300px;
  .description {
    word-break: normal !important;
    text-align: left;
  }
  hr {
    margin-bottom: 1em;
    border: 0;
    height: 1px;
    background: #333;
    background-image: linear-gradient(to right, #ccc, #333, #ccc);
  }
  img.small-image {
    max-width: 100%;
    max-height: 9em;
    margin-top: 2em;
    cursor: pointer;
  }
  img.big-image {
    max-width: 100%;
  }

  .text-column {
    text-align: left;
    h3 {
      text-align: center;
      .fa-icon {
        margin-bottom: -0.2em;
      }
    }
    a {
      &:hover {

      }

      color: black;
      text-decoration: none;
      .filename {
        display: inline-block;
        margin-left: 0.5em;
      }
    }
  }
}
</style>
