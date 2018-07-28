import Vue from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import fontawesome from '@fortawesome/fontawesome'
import faBook from '@fortawesome/fontawesome-free-solid/faBook'
import faCodeBranch from '@fortawesome/fontawesome-free-solid/faCodeBranch'
import faFlask from '@fortawesome/fontawesome-free-solid/faFlask'
import faList from '@fortawesome/fontawesome-free-solid/faList'
import faShoppingCart from '@fortawesome/fontawesome-free-solid/faShoppingCart'
import faRecycle from '@fortawesome/fontawesome-free-solid/faRecycle'
import faShareAlt from '@fortawesome/fontawesome-free-solid/faShareAlt'
import faTrashAlt from '@fortawesome/fontawesome-free-solid/faTrashAlt'
import faUserCircle from '@fortawesome/fontawesome-free-solid/faUserCircle'
import faFileCode from '@fortawesome/fontawesome-free-solid/faFileCode'

fontawesome.library.add(
  faFlask,
  faBook,
  faCodeBranch,
  faTrashAlt,
  faList,
  faUserCircle,
  faShoppingCart,
  faShareAlt,
  faRecycle,
  faFileCode
)

Vue.component('font-awesome-icon', FontAwesomeIcon)
