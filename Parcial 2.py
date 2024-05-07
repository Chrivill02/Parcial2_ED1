class TreeNode:
    def __init__(self, data):
        self.data = data
        self.yes = None
        self.no = None


class GuessingGame:
    def __init__(self):
        self.root = None

    def build_tree(self):
        self.root = TreeNode("¿Es un animal?")
        self.root.yes = TreeNode("¿Tiene cuatro patas?")
        self.root.no = TreeNode("¿Es un vehículo?")
        self.root.yes.yes = TreeNode("Perro")
        self.root.yes.no = TreeNode("Gato")
        self.root.no.yes = TreeNode("Avión")
        self.root.no.no = TreeNode("Barco")

    def play(self):
        current_node = self.root
        parent_node = None
        while current_node.yes and current_node.no:
            parent_node = current_node
            answer = input(current_node.data + " (sí/no): ").lower()
            if answer == 'sí':
                current_node = current_node.yes
            elif answer == 'no':
                current_node = current_node.no
            else:
                print("Por favor, responde con 'sí' o 'no'.")
        guess = current_node.data
        answer = input("¿Es un/a {}? (sí/no): ".format(guess)).lower()
        if answer == 'sí':
            print("¡Gané!")
        else:
            new_guess = input("¿Qué era entonces? ")
            new_question = input(
                "Por favor, ingresa una pregunta que distinguirá un/a {} de un/a {}: ".format(new_guess, guess))
            new_answer = input("¿Cuál es la respuesta a tu pregunta? (sí/no): ").lower()

            # Actualizar el árbol con la nueva pregunta y respuesta
            new_node = TreeNode(new_question)
            if new_answer == 'sí':
                new_node.yes = TreeNode(new_guess)
                new_node.no = TreeNode(guess)
            else:
                new_node.yes = TreeNode(guess)
                new_node.no = TreeNode(new_guess)

            if parent_node:
                if parent_node.yes == current_node:
                    parent_node.yes = new_node
                else:
                    parent_node.no = new_node
            else:
                self.root = new_node

        play_again = input("¿Quieres jugar de nuevo? (sí/no): ").lower()
        if play_again == 'sí':
            self.build_tree()
            self.play()

    def export_tree(self, filename):
        with open(filename, 'w') as file:
            file.write(self.preorder(self.root) + '\n')
            file.write(self.inorder(self.root) + '\n')
            file.write(self.postorder(self.root) + '\n')

    def preorder(self, node):
        if node is None:
            return ''
        return str(node.data) + ' ' + self.preorder(node.yes) + ' ' + self.preorder(node.no)

    def inorder(self, node):
        if node is None:
            return ''
        return self.inorder(node.yes) + ' ' + str(node.data) + ' ' + self.inorder(node.no)

    def postorder(self, node):
        if node is None:
            return ''
        return self.postorder(node.yes) + ' ' + self.postorder(node.no) + ' ' + str(node.data)

    def import_tree(self, filename):
        with open(filename, 'r') as file:
            preorder = file.readline().strip().split()
            inorder = file.readline().strip().split()
            self.root = self.construct_tree(preorder, inorder)

    def construct_tree(self, preorder, inorder):
        if not preorder:
            return None
        root_value = preorder[0]
        root_index = inorder.index(root_value)
        root = TreeNode(root_value)
        root.yes = self.construct_tree(preorder[1:root_index + 1], inorder[:root_index])
        root.no = self.construct_tree(preorder[root_index + 1:], inorder[root_index + 1:])
        return root


# Ejemplo de uso del juego
game = GuessingGame()
game.build_tree()
game.play()
game.export_tree("arbol.txt")

# Preguntar si quiere jugar de nuevo después de agregar respuestas del usuario a build_tree
play_again = input("¿Quieres jugar de nuevo? (sí/no): ").lower()
if play_again == 'sí':
    game.build_tree()
    game.play()
