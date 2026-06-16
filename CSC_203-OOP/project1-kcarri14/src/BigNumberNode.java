/**
 * A partial 'Node' class. Modify as necessary.
 *
 * @author Vanessa Rivera
 */
class BigNumberNode {
    private int data;
    private BigNumberNode next;


    public BigNumberNode(int data) {
        this.data = data;
        this.next = null;
    }
    public int getData(){
        return data;
    }
    public BigNumberNode getNext(){
        return next;
    }
    public void setNext(BigNumberNode next){
        this.next = next;
    }



}