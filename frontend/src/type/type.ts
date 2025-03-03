type Lang = "ja";

type ItemBaseType = "vocab" | "grammar";

type ItemBase<T extends ItemBaseType> = {
    type: T;
    content: string;
    lang: Lang;
    translation: string;
    description: string;
    examples: string[];
    correctCount: number;
    wrongCount: number;
};

export type VocabItem = ItemBase<"vocab"> & {
    id: number;
};

export type GrammarItem = {
    id: number;
    content: string;
    lang: Lang;
    translation: string;
    points: ItemBase<"grammar">[];
};
