import express    from 'express'
import { resolve } from 'path'
import bodyParser from 'body-parser'
import { log }    from 'mulan-lib'
import { port }   from 'config'
import defineApi  from './api'
import validator  from './middleware/validator'
import { ROOT_PATH } from 'config/path'


const server =
defineApi(
  express()
  .use(bodyParser.json())
  .use(bodyParser.urlencoded({ extended: true }))
  // .use(validator())
)
.use('/', express.static(resolve(ROOT_PATH, 'public')))

server.listen(port, () => log('seed run at ' + port))
