let mediaRecorder
let audioChunks=[]
let stream

const startBtn=document.getElementById("start-btn")
const stopBtn=document.getElementById("stop-btn")

startBtn.onclick=async()=>{

try{

stream=await navigator.mediaDevices.getUserMedia({audio:true})

mediaRecorder=new MediaRecorder(stream)

mediaRecorder.ondataavailable=e=>{
audioChunks.push(e.data)
}

mediaRecorder.onstop=()=>{

const blob=new Blob(audioChunks,{type:"audio/webm"})

const url=URL.createObjectURL(blob)

document.getElementById("audio-playback").src=url

document.getElementById("audio-playback").classList.remove("d-none")

audioChunks=[]

}

mediaRecorder.start()

startBtn.disabled=true
stopBtn.disabled=false

}catch(err){

alert("Microphone access denied: "+err)

}

}


stopBtn.onclick=()=>{

mediaRecorder.stop()

stream.getTracks().forEach(track=>track.stop())

startBtn.disabled=false
stopBtn.disabled=true

}