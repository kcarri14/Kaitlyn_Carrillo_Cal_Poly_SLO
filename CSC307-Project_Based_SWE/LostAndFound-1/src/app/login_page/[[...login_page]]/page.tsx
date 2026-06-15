import "@/app/login_page/[[...login_page]]/login.css"
import Link from 'next/link';
import { SignIn } from '@clerk/nextjs'
export default function Login(){
    return (
        <div>
            <div className="content">
        
            <div className="center"><SignIn /></div>
            <div className="break"></div>
            <div className="center"><Link href="/forgot_password_page">Forgot Password?</Link></div>
            <div className="break"></div>
            {/* <div className="center"><Link href="/">Continue as Guest</Link></div> */}
            </div>
        </div>
    )
}

