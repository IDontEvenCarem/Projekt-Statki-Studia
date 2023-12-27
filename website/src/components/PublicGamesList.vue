<template>
    <div class="wrapper">
        <h2>Publiczne gry</h2>
        <table>
            <thead>
                <tr>
                    <th>Nazwa gry</th>
                    <th>Gracze</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Test</td>
                    <td>2/4</td>
                    <td><button>Dołącz</button></td>
                </tr>
                <tr>
                    <td>Test</td>
                    <td>2/4</td>
                    <td><button>Dołącz</button></td>
                </tr>
                <tr>
                    <td>Test</td>
                    <td>2/4</td>
                    <td><button>Dołącz</button></td>
                </tr>
                <tr>
                    <td>Test</td>
                    <td>2/4</td>
                    <td><button>Dołącz</button></td>
                </tr>
                <tr>
                    <td>Test</td>
                    <td>2/4</td>
                    <td><button>Dołącz</button></td>
                </tr>
                <tr>
                    <td>Test</td>
                    <td>2/4</td>
                    <td><button>Dołącz</button></td>
                </tr>
                <tr>
                    <td>Test</td>
                    <td>2/4</td>
                    <td><button>Dołącz</button></td>
                </tr>
                <tr>
                    <td>Test</td>
                    <td>2/4</td>
                    <td><button>Dołącz</button></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
.wrapper {
    display: grid;
    grid-template: max-content 1fr / 1fr;
    gap: 0.25em;
    place-items: center;
    text-align: center;
    background-color: color-mix(in srgb, var(--main-color) 75%, #000);
    border-radius: var(--border-radius);
    filter: drop-shadow(-4px 4px 5px color-mix(in srgb, var(--main-color) 50%, #000));
    padding: 1em;
    width: fit-content;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
}

table {
    width: 100%;
    border-collapse: collapse;
}

thead {
    background-color: color-mix(in srgb, var(--main-color) 50%, #000);
    color: var(--main-color-light);
}

th, td {
    padding: 0.5em;
}

tbody tr:nth-child(2n) {
    background-color: color-mix(in srgb, var(--main-color) 70%, #000);
}

</style>
