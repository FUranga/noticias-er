import Link from "next/link";

function fechaHoy(): string {
  const f = new Date().toLocaleDateString("es-AR", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  return f.charAt(0).toUpperCase() + f.slice(1);
}

export function Header() {
  return (
    <header>
      <div className="font-ui flex items-center justify-between border-b border-neutral-300 px-4 py-1.5 text-[0.7rem] text-neutral-500 sm:px-8">
        <span>{fechaHoy()}</span>
        <span>Paraná, Entre Ríos</span>
      </div>
      <div className="px-4 py-8 text-center sm:px-8">
        <Link href="/" className="block">
          <span className="font-headline text-4xl font-bold tracking-tight sm:text-5xl">
            Agencia Entrerriana
          </span>
        </Link>
        <p className="font-ui mt-2 text-xs uppercase tracking-[0.2em] text-neutral-500">
          Noticias de Paraná y la provincia
        </p>
      </div>
      <div className="border-b-2 border-neutral-900" />
    </header>
  );
}
