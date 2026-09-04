import Link from "next/link";

export function Header() {
  return (
    <header className="border-b border-neutral-200">
      <div className="mx-auto max-w-3xl px-4 py-6">
        <Link href="/" className="block text-center">
          <span className="font-serif text-3xl font-semibold tracking-tight">
            [NOMBRE DEL MEDIO]
          </span>
          <span className="mt-1 block text-xs uppercase tracking-widest text-neutral-500">
            Política y economía de Paraná y Entre Ríos
          </span>
        </Link>
      </div>
    </header>
  );
}
