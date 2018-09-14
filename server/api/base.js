import reply from 'lib/reply'

export default (
  router =>
  router
  .all('/t', (req, res) => {
    reply(res, () => {
      const { body, query } = req
      return { body, query }
    })
  })
  .get('/heartbeat', (req, res) => {
    reply(res, () => 1)
  })
)
