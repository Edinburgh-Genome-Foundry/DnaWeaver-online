export default function install (Vue) {
  Vue.component('backend-querier', require('./BackendQuerier').default)
  Vue.component('progress-bars', require('./ProgressBars').default)
  // Vue.component('learn-more', require('./LearnMore').default)
  Vue.component('download-button', require('./DownloadButton').default)
  // Vue.component('helper', require('./Helper').default)
  Vue.component('files-uploader', require('./FilesUploader').default)
  Vue.component('detail-slider', require('./DetailSlider').default)

  // Vue.component('collapsible', require('./Collapsible').default)
  Vue.component('file-example', require('./FileExample').default)
  // Vue.component('web-links', require('./WebLinks').default)
}
