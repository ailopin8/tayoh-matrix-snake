// One authority per mode: local Python service, or the same Python in a worker.
let worker, counter=0;
const pending=new Map();
const configuration=fetch(new URL('./runtime-config.json',import.meta.url)).then(r=>r.ok?r.json():{mode:'server'});
export const mode=configuration.then(c=>c.mode);
function workerRequest(path,body){
  if(!worker){
    worker=new Worker(new URL('./python-worker.js',import.meta.url));
    worker.onmessage=e=>{const p=pending.get(e.data.id);if(!p)return;pending.delete(e.data.id);e.data.error?p.reject(Error(e.data.error)):p.resolve(e.data.result);};
    worker.onerror=e=>{for(const p of pending.values())p.reject(Error('Python worker failed: '+e.message));pending.clear();};
  }
  return new Promise((resolve,reject)=>{const id=++counter;pending.set(id,{resolve,reject});worker.postMessage({id,path,body});});
}
export async function request(path,body){
  if(await mode==='browser-python')return workerRequest(path,body);
  const r=await fetch(path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  const s=await r.json();if(!r.ok)throw Error(s.error||r.status);return s;
}
export async function download(kind){
  const data=await request('/api/'+kind),url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download=kind==='replay'?'tayoh-replay.json':'tayoh-outcome.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
