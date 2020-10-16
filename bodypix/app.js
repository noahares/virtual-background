const tf = require('@tensorflow/tfjs-node');
const bodyPix = require('@tensorflow-models/body-pix');
const http = require('http');

(async () => {
  const net = await bodyPix.load();
  const server = http.createServer();
  server.on('request', async (req, res) => {
    var chunks = [];
    req.on('data', (chunk) => {
      chunks.push(chunk);
    });
    req.on('end', async () => {
      const image = tf.node.decodeImage(Buffer.concat(chunks));
      segmentation = await net.segmentPerson(image);
      res.writeHead(200, { 'Content-Type': 'application/octet-stream' });
      res.write(Buffer.from(segmentation.data));
      res.end();
      tf.dispose(image);
    });
  });
  server.listen(9000);
})();
