import express from 'express'
import { log } from 'mulan-lib'
import baseApi from './base'

export default (
  server =>
  server
    .use('/api',     baseApi(express.Router()))
)
