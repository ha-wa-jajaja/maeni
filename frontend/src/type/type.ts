type Lang = "ja";

type ItemBaseType = "vocab" | "grammar";

type ItemBase<T extends ItemBaseType> = {
    id: number;
    type: T;
    content: string;
    lang: Lang;
    translation: string;
    description: string;
    correctCount: number;
    wrongCount: number;
};

export type Example = {
    id: number;
    content: string;
    lang: Lang;
    translation: string;
    description: string | null;
    points: Array<ItemBase<"vocab" | "grammar">>;
};
