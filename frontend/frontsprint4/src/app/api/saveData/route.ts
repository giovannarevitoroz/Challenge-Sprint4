import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
export async function POST(request: Request) {
    const data = await request.json();
    const filePath = path.join(process.cwd(), 'src', 'data', 'dadosCadastro.json');
    try {
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
        return NextResponse.json({ message: 'Dados salvos com sucesso!' });
    } catch (error) {
        console.error('Erro ao salvar dados:', error);
        return NextResponse.json({ message: 'Erro ao salvar dados' }, { status: 500 });
    }
}